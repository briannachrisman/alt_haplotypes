from scipy.stats import poisson
import pandas as pd
import numpy as np
from glob import glob

def GlobalInterval(L, prob_thresh=.95):
    print('global babay')
    '''
        Returns the tightest genomic region where the probability of a k-mer occuring is at least prob_thresh, given the likelihoods L at each region.
                Parameters:
                        L (array): Array of likelihoods for each global genomic region.
                        prob_thresh (float): Minimum probability that a set of genomic regions contains a k-mer.

                Returns:
                        interval (tuple): The start and end idxs of the tightest global genomic region where the probability of a k-mer residing is at least prob_thresh.
        '''    
    
    P = 2**(L-max(L))
    P = P/sum(P)
    cumsum = np.cumsum(P)
    smallest_end = np.where(cumsum>prob_thresh)[0][0]
    cumsum = np.cumsum(P[::-1])[::-1]
    largest_start = np.where(cumsum>prob_thresh)[0][-1]

    shortest_segment = min(smallest_end, len(P)-largest_start)
    interval = (np.nan,np.nan)
    for start in [s for s in range(largest_start)][::-1]:
        for end in range(smallest_end, start+shortest_segment):
            if (sum(P[start:end])>prob_thresh) & ((end-start)<shortest_segment):
                shortest_segment = end-start
                interval = (start,end)
                prob = sum(P[start:end])
                break
        if (smallest_end-start)>=shortest_segment: break
    return (start, end)




class MLE:
    def __init__(self, avg_kmer_depth, poisson_cache_length, eps=0):
        print('initializing')
        self.poisson_cache = [[], []]
        self.avg_kmer_depth=avg_kmer_depth
        self.poisson_cache[0] = [poisson.pmf(k=k, mu=avg_kmer_depth) for k in range(poisson_cache_length)]
        self.poisson_cache[1] = [poisson.pmf(k=k, mu=2*avg_kmer_depth) for k in range(poisson_cache_length)]
        self.cached_family_log_likelihood = dict()
        self.eps = eps
        
        
        
        
        
    def cached_poisson_pmf(self,k,g):
        if (g==0) & (k!=0):
            return self.eps
        if (k==0) & (g==0): 
            return 1-3*self.eps #poisson.pmf(g*avg_kmer_depth, k)
        else:
            return min(max(self.poisson_cache[g-1][k], self.eps), 1-3*self.eps)
    
    
    
    
    
    def family_log_likelihood(self,k_m, k_p, k_cs, phases_ch):

        '''
        Returns the probability of a k-mer distribution in a family given the each member's kmer counts and the children's phasings. Note: takes about 1 second per 50K family-regions.

                Parameters:
                        k_m (int): mom_kmer_count (int): A decimal integer
                        k_p (int): dad_kmer_count (int): Another decimal integer
                        phases_ch (list): A list of of tuples representing each child's phasings (mom's chromome, dad's chromosme) {(0,0), (0,1), (1,0), (1,1)}
                        avg_kmer_depth (int): Mean for avg k-mer depth of poisson distribution.

                Returns:
                        log likelihood (float): The log of the probability of the family's k-mer distribution given the famiy genotypes.
        '''    

        key = tuple(sorted([(k_m, k_p, k,g[0], g[1]) for k,g in zip(k_cs, phases_ch)]))
        if key in self.cached_family_log_likelihood: log_P = self.cached_family_log_likelihood[key]
        else:
            possible_gs = [(0,0), (1,1), (0,1), (1,0)]
            log_P_m = np.log2(sum([self.cached_poisson_pmf(k_m, g) for g in [0,1,1,2]]))
            log_P_p= np.log2(sum([self.cached_poisson_pmf(k_p, g) for g in [0,1,1,2]]))
            log_P_ch = np.log2(sum([self.cached_poisson_pmf(k_m,sum(g_m))*self.cached_poisson_pmf(k_p,sum(g_p))*
                                    np.prod([self.cached_poisson_pmf(k_c, g_m[phase_ch[0]]+g_p[phase_ch[1]]) 
                                             for k_c, phase_ch in zip(k_cs, phases_ch)]) for g_p in possible_gs for g_m in possible_gs]))
            log_P = log_P_ch-log_P_m-log_P_p
            self.cached_family_log_likelihood[key] = log_P

            if log_P>0: print("ERROR: log likelihood cannot be > 0")
        return log_P
    
    
    
    
    
    def GlobalLikelihood(self,kmer_counts, bam_mappings, family_info, global_region_to_idx, fam_region_to_idx, fam_idx_to_global_idx, MAX_FAMS=100):
        final_likelihoods = {}
        families_in_file = [i.replace('.txt', '').split('/')[-1] for i in glob(
            '/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/*.txt')]
        sample_id_to_participant = {sample_id:participant_id for participant_id, sample_id in zip(bam_mappings.participant_id, bam_mappings.index)}
        for k in kmer_counts.iterrows():
            print(k[0])
            global_likelihoods = [] #np.zeros(len(global_region_to_idx)) 
            fams_included = set(bam_mappings.loc[kmer_counts.columns[k[1]>0]].family).intersection(family_info.index).intersection(families_in_file)
            for fam in (list(fams_included)[:MAX_FAMS]):  
                global_likelihood = np.zeros(len(global_region_to_idx)) 


                # Extract mom, dad, and child sample_ids.
                children = family_info.loc[fam].sib_samples
                mom = family_info.loc[fam].mother_sample
                dad = family_info.loc[fam].father_sample
                phased_fam = pd.read_csv('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/%s.txt' % fam,
                                         sep='\t')

                # Skip family if dataframe is weird.
                missing_children=False
                for ch in children:
                    if sample_id_to_participant[ch] + '_mat' not in phased_fam.columns: 
                        missing_children=True
                        break
                if missing_children: continue
                
                # Set up phasing dataframe.
                for ch in children:
                    phased_fam[ch] = [(m,d-2) for m,d in zip(phased_fam[sample_id_to_participant[ch]+'_mat'], phased_fam[sample_id_to_participant[ch]+'_pat'])]
                phased_fam.index = ['%s.%09d.%09d' % (('0' + chrom[3:])[-2:].replace('0X', 'XX'), start, end) for chrom, start, end in phased_fam[['chrom', 'start_pos', 'end_pos']].values]
                #phased_fam = phased_fam[children]

                # Compute family likelihood.
                fam_likelihood = [self.family_log_likelihood(k[1][mom], k[1][dad], k[1][children], phased_fam[children].iloc[i]) for i in range(len(phased_fam))]

                # Convert family likelihood region to global region. 
                for i,l in enumerate(fam_likelihood):
                    global_idxs = fam_idx_to_global_idx[fam_region_to_idx[phased_fam.index[i]]]
                    global_likelihood[global_idxs] =  l
                global_likelihood[global_likelihood==0] = np.mean(global_likelihood[global_likelihood!=0])
                global_likelihoods = global_likelihoods + [global_likelihood]

            final_likelihoods[k[0]] = np.array(global_likelihoods).sum(axis=0)
            #try:
            #    print(GlobalInterval(final_likelihoods[k[0]]))
            #except: donothing=True
            #print([idx_to_global_region[i] for i in np.argsort(final_likelihood)[::-1][:100:10]])
        return final_likelihoods

