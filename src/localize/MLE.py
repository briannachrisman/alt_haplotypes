from scipy.stats import poisson
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
from Bio import SeqIO
from collections import Counter
import matplotlib.pyplot as plt
from glob import glob
import json
import pickle

def GlobalInterval(L, prob_thresh=.95):
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
    #return (largest_start, smallest_end)
    if idx_to_global_region[smallest_end][:2] != idx_to_global_region[largest_start][:2]:  return (largest_start, smallest_end) # > 1000: return (0, len(idx_to_global_region)-1)
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
    def __init__(self, avg_kmer_depth, poisson_cache_length, eps=0, phasing_error=.05):
        self.poisson_cache = [[], []]
        self.avg_kmer_depth=avg_kmer_depth
        self.poisson_cache[0] = [poisson.pmf(k=k, mu=avg_kmer_depth) for k in range(poisson_cache_length)]
        self.poisson_cache[1] = [poisson.pmf(k=k, mu=2*avg_kmer_depth) for k in range(poisson_cache_length)]
        self.cached_family_log_likelihood = dict()
        self.eps = eps
        self.phasing_error=phasing_error
        with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'rb') as f:
            self.phased_fam_dict = pickle.load(f)

            
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

        #key = tuple(sorted([(k_m, k_p, k,g[0], g[1]) for k,g in zip(k_cs, phases_ch)]))
        key = tuple([(k_m, k_p, k,g[0], g[1]) for k,g in zip(k_cs, phases_ch)])
        # TODO ADD TO KEY
        #if key in self.cached_family_log_likelihood: log_P = self.cached_family_log_likelihood[key]
        #else:
        if True:
            possible_gs = [(0,0), (1,1), (0,1), (1,0)]
            #log_P_m = np.log2(sum([self.cached_poisson_pmf(k_m, g) for g in [0,1,1,2]]))
            #log_P_p= np.log2(sum([self.cached_poisson_pmf(k_p, g) for g in [0,1,1,2]]))
            log_P_ch = np.log2(sum([self.cached_poisson_pmf(k_m,sum(g_m))*self.cached_poisson_pmf(k_p,sum(g_p))*
                                    np.prod([self.cached_poisson_pmf(k_c, g_m[phase_ch[0]]+g_p[phase_ch[1]]) 
                                             for k_c, phase_ch in zip(k_cs, phases_ch)]) for g_p in possible_gs for g_m in possible_gs]))
            log_P = log_P_ch#-log_P_m-log_P_p
            #self.cached_family_log_likelihood[key] = log_P

            if log_P>0: print("ERROR: log likelihood cannot be > 0")
        return log_P
    
    
    
    
    
    def GlobalLikelihood(self,kmer_count, bam_mappings, family_info, global_region_to_idx, fam_region_to_idx, fam_idx_to_global_idx, MAX_FAMS=None):
        global_likelihoods = [] #np.zeros(len(global_region_to_idx)) 
        fams_included = set(bam_mappings.loc[np.array(kmer_count[1].keys())[kmer_count[1].values>0]].family).intersection(self.phased_fam_dict.keys())
        if MAX_FAMS: fams_included = list(fams_included)[:min(MAX_FAMS, len(fams_included))]
        for fam in fams_included:
            
            # Initialize global likelihood
            global_likelihood = np.zeros(len(global_region_to_idx)) 


            # Extract mom, dad, and child sample_ids.
            children = family_info.loc[fam].sib_samples
            mom = family_info.loc[fam].mother_sample
            dad = family_info.loc[fam].father_sample
            phased_fam = self.phased_fam_dict[fam]

            # Compute likelihood of family's k-mer distribution for each phasing configuration.
            fam_likelihood = np.zeros(len(phased_fam))
            phasings = [tuple(phased_fam[children].iloc[i].values) for i in range(len(phased_fam))]
            possible_phasings = set(phasings)
            phasing_ps = np.array([2**self.family_log_likelihood(kmer_count[1][mom], kmer_count[1][dad], kmer_count[1][children], phase) 
                          for phase in possible_phasings])
            phasing_ps = self.phasing_error*(sum(phasing_ps) - phasing_ps) + (1-self.phasing_error)*phasing_ps
            for phase, phase_p in zip(possible_phasings, phasing_ps):   
                idx = np.where([p==phase for p in phasings])[0]
                fam_likelihood[idx] = np.log2(phase_p)
            
            
            #for phase in possible_phasings:
            #    idx = np.where([p==phase for p in phasings])[0]
            #    fam_likelihood[idx] = self.family_log_likelihood(kmer_count[1][mom], kmer_count[1][dad], kmer_count[1][children], phase) #for i in range(len(phased_fam))
            #print(min(fam_likelihood), max(fam_likelihood))
            
            
            # Convert family likelihood region to global region. 
            for i,l in enumerate(fam_likelihood):
                global_idxs = fam_idx_to_global_idx[fam_region_to_idx[phased_fam.index[i]]]
                global_likelihood[global_idxs] =  l
                
            # For regions with unknown phasings in the current family, default to the median likelihood across the rest of the genome.
            global_likelihood[global_likelihood==0] = np.median(global_likelihood[global_likelihood!=0])
            global_likelihoods = global_likelihoods + [global_likelihood]

        return np.array(global_likelihoods).sum(axis=0)
