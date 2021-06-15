import itertools
import pickle
import numpy as np
from scipy.stats import poisson
import time
import sys
import pandas as pd

N_PHASE = int(sys.argv[1])
#import multiprocessing as mp

eps = np.log2(.0001)
max_count = 25+1
kmer_length = 100


BAM_MAPPINGS_FILE = '/home/groups/dpwall/briannac/general_data/bam_mappings.csv'

# Construct average k-mer depth dictionary.
bam_mappings = pd.read_csv(BAM_MAPPINGS_FILE, sep='\t', index_col=1)
bam_mappings = bam_mappings[bam_mappings['status']=='Passed_QC_analysis_ready']
PARENT_DIR = '/home/groups/dpwall/briannac/blood_microbiome/'
ihart_flagstat_file = PARENT_DIR + 'data/ihart_flagstat.csv'
flagstat = pd.read_csv(ihart_flagstat_file, index_col=0)
flagstat = flagstat.loc[set(flagstat.index).intersection(bam_mappings.index)]
bam_mappings = bam_mappings.loc[flagstat.index]
total_mapped_reads = flagstat.ProperPair*((flagstat.Total_Reads-flagstat.Supplementary-flagstat.Duplicates)/flagstat.Total_Reads)
avg_coverage = total_mapped_reads*150/(6.27e9)#*(bam_mappings.sex_numeric.astype(float)==1.0) + 6.37e9*(bam_mappings.sex_numeric.astype(float)==2.0))
avg_n_100mers = (150-kmer_length)/(150/avg_coverage)
kmer_depth_dict = {k:avg_n_100mers[k] for k in avg_n_100mers.keys()}


with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'rb') as f:
    phased_fam_dict = pickle.load(f)

    
    
all_family_phasings = set()
for f in phased_fam_dict:
    fam_phases = phased_fam_dict[f]
    all_family_phasings = all_family_phasings.union(set([tuple(v) for v in fam_phases.values]))
    
    
poisson_cache = [[], []]
avg_kmer_depth=np.mean(list(kmer_depth_dict.values()))

poisson_cache[0] = [poisson.pmf(k=k, mu=avg_kmer_depth) for k in range(max_count)]
poisson_cache[1] = [poisson.pmf(k=k, mu=2*avg_kmer_depth) for k in range(max_count)]

def cached_poisson_pmf(k,g):
    return min(max(poisson_cache[g-1][k], eps), 1-3*eps)

def Probabilities(phases_ch):
    possible_gs = [(0,0),(0,1), (1,0), (1,1)]
    family_probability_cache = dict()
    for k_m in range(max_count): # Iterate through possible k-mer counts for mom.  (up to 30)
        print(k_m/max_count)
        for k_p in range(max_count): # Iterate through possible k-mer counts for dad (up to 30.)
            for k_cs in itertools.combinations_with_replacement(range(max_count), len(phases_ch)): # Iterate through possible k-mer counts for children (up to 30.)
                family_probability_cache[(k_m, k_p, k_cs, phases_ch)] = np.log2(sum(
                    [cached_poisson_pmf(k_m,sum(g_m))*
                     cached_poisson_pmf(k_p,sum(g_p))*
                     np.prod([cached_poisson_pmf(k_c, g_m[phase_ch[0]]+g_p[phase_ch[1]]) for k_c, phase_ch in zip(k_cs, phases_ch)]
                            ) for g_p in possible_gs for g_m in possible_gs]))
    return family_probability_cache

#pool = mp.Pool(mp.cpu_count())

#dicts = pool.map(Probabilities, list(all_family_phasings))
#pool.close()
family_probability_dict = Probabilities(list(all_family_phasings)[N_PHASE])
#for d in dicts:
#    family_probability_dict.update(d)

with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/family_probability_cache_%i.pickle' % N_PHASE, 'wb') as f:
        pickle.dump(family_probability_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

