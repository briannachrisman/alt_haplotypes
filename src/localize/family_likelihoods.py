import time
import pandas as pd
import numpy as np
from tqdm import tqdm
from Bio import SeqIO
from collections import Counter
import matplotlib.pyplot as plt
from glob import glob
import json
import sys
import pickle
import numpy as np
from scipy.stats import poisson
import time
import sys
import pandas as pd

# Set up file locations.
IDX = int(sys.argv[1])
OUT_DIR = sys.argv[2] # /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/ground_truth/
KMER_COUNTS_FILE = sys.argv[3] #'/home/groups/dpwall/briannac/alt_haplotypes/data/known_kmer_counts.tsv'
N_KMERS = int(sys.argv[4]) #1094247 # Number of kmers in KMER_COUNTS_FILE file


PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/'
BAM_MAPPINGS_FILE = '/home/groups/dpwall/briannac/general_data/bam_mappings.csv'


###################################################################
#################### Loading files. ##############################
###################################################################
print("Loading in files...")
# Load in family region/global region conversion data.
fam_region_to_idx = np.load(PHASINGS_DIR +  'fam_region_to_idx.npy', allow_pickle=True).item()
idx_to_fam_region = np.load(PHASINGS_DIR +  'idx_to_fam_region.npy', allow_pickle=True).item()
global_region_to_idx = np.load(PHASINGS_DIR +  'global_region_to_idx.npy', allow_pickle=True).item()
idx_to_global_region = np.load(PHASINGS_DIR +  'idx_to_global_region.npy', allow_pickle=True).item()
fam_idx_to_global_idx = np.load(PHASINGS_DIR + 'fam_regions_to_global_regions.npy', allow_pickle=True)
family_info = pd.read_pickle(PHASINGS_DIR + 'fam_list.df')

# Info from BAM mappings.
bam_mappings = pd.read_csv(BAM_MAPPINGS_FILE, sep='\t', index_col=1)
bam_mappings = bam_mappings[bam_mappings['status']=='Passed_QC_analysis_ready']


# Load in k-mer counts.
family = family_info.index[IDX]
print('family ', family)
samples = [family_info.iloc[IDX]['mother_sample'], family_info.iloc[IDX]['father_sample']] +  family_info.iloc[IDX]['sib_samples']
bam_mappings['counter_idx'] = [i for i in range(len(bam_mappings))]
cols_in_df = bam_mappings.loc[samples].counter_idx.values
print(samples)
###################################################################
#### Prep dict for normalizing k-counts by sample read depth. #####
###################################################################
kmer_length=100
ihart_flagstat_file = '/home/groups/dpwall/briannac/blood_microbiome/data/ihart_flagstat.csv'
flagstat = pd.read_csv(ihart_flagstat_file, index_col=0)
flagstat = flagstat.loc[set(flagstat.index).intersection(bam_mappings.index)]
sex = bam_mappings.loc[flagstat.index].sex_numeric
#bam_mappings = bam_mappings.loc[set(flagstat.index).intersection(bam_mappings.index)]
total_mapped_reads = flagstat.ProperPair*((flagstat.Total_Reads-flagstat.Supplementary-flagstat.Duplicates)/flagstat.Total_Reads)
avg_coverage = total_mapped_reads*150/(6.27e9*(sex.astype(float)==1.0) + 6.37e9*(sex.astype(float)==2.0))
avg_n_100mers = (150-kmer_length)/(150/avg_coverage)
kmer_depth_dict = {k:avg_n_100mers[k] if k in avg_n_100mers else np.mean(avg_n_100mers.values) for k in bam_mappings.index}
avg_k_depth = np.mean(list(kmer_depth_dict.values()))



###########################################################
####### Set up poisson cache and access function. ########
###########################################################
print("Setting up poisson cache...")
max_count = 100
eps = 0
with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'rb') as f:
    phased_fam_dict = pickle.load(f)
family_phasings = sorted(list(set([tuple(v) for v in phased_fam_dict[family].values])))
poisson_cache = [[], []]
avg_kmer_depth=np.mean(list(kmer_depth_dict.values()))
poisson_cache[0] = [poisson.pmf(k=k, mu=avg_kmer_depth) for k in range(max_count)]
poisson_cache[1] = [poisson.pmf(k=k, mu=2*avg_kmer_depth) for k in range(max_count)]

def cached_poisson_pmf(k,g):
    if (g==0) & (k!=0): return eps
    if (g==0) & (k==0): return 1-3*eps
    if k>=max_count: return eps
    return min(max(poisson_cache[g-1][k], eps), 1-3*eps)



###########################################################
#### Computing phasing x global region Presence matrix ####
###########################################################
print("Computing phasing x global region presence matrix...")
family_phasings_to_idx_dict = {p:i for i,p in enumerate(family_phasings)}
global_regions_phasings_fam = np.zeros((len(global_region_to_idx),len(family_phasings))) 

for k,v in pd.DataFrame(phased_fam_dict[family].apply(lambda x: tuple(x), axis=1)).iterrows():
    for i in fam_idx_to_global_idx[fam_region_to_idx[k]]:
        global_regions_phasings_fam[i,family_phasings_to_idx_dict[v[0]]] = 1
        
# If we don't know the phasing, then default to most common phasing.
# Doing it this way will assign unknown regions the most common likelihood of the whole family's genome.
# If we didn't do this, we would end up with have the likelihood=0 at regions w/unknown phases, this will give unknown regions an unfair advantage.
impute_vector = np.zeros(len(family_phasings))
impute_vector[np.argmax(global_regions_phasings_fam.sum(axis=0))] = 1

#impute_vector = np.apply_along_axis(arr=global_regions_phasings_fam[np.where(global_regions_phasings_fam.sum(axis=1)!=0)[0], :], func1d=np.median, axis=0)
for i in np.where(global_regions_phasings_fam.sum(axis=1)==0)[0]:
    global_regions_phasings_fam[i,:]=impute_vector



###########################################################
###### Computing phasing x k-mer Likelihood matrix ########
###########################################################
print("Computing phasing x k-mer region likelihood matrix...")
phases_kmers_L = np.zeros((N_KMERS,len(family_phasings)))  # Initializ likelihood matrix (phases as rows, kmers as columns)
chunks = pd.read_table(KMER_COUNTS_FILE, header=None,  chunksize=10000, usecols=1+cols_in_df, nrows=N_KMERS)
for kmer_counts in chunks:
    kmer_counts = kmer_counts[1+cols_in_df]
    kmer_counts.columns = samples
    print(kmer_counts.index[0])
    norm_mult = np.array([avg_k_depth/kmer_depth_dict[c] for c in kmer_counts.columns])
    kmer_counts = kmer_counts[((kmer_counts>0).sum(axis=1)>0)]
    kmer_counts_normed = kmer_counts.apply(lambda x: round(x*norm_mult), axis=1).astype(int)
    poss_kmer_counts = set([tuple(v) for v in kmer_counts_normed.values])
    family_probability_cache = dict()
    for phases_ch in family_phasings:
        possible_gs = [(0,0), (0,1), (1,0), (1,1)]
        for kmer_count_set in poss_kmer_counts:
            k_m = kmer_count_set[0]
            k_p = kmer_count_set[1]
            k_cs = kmer_count_set[2:]
            family_probability_cache[((k_m, k_p, *k_cs), phases_ch)] = round(np.log2(sum(
                [cached_poisson_pmf(k_m,sum(g_m))*
                 cached_poisson_pmf(k_p,sum(g_p))*
                 np.prod([cached_poisson_pmf(k_c, g_m[phase_ch[0]]+g_p[phase_ch[1]]) for k_c, phase_ch in zip(k_cs, phases_ch)]
                        ) for g_p in possible_gs for g_m in possible_gs])),3)

    print('Done making cached dictionary.')
    # Compute likelihood matrix (phasings x kmers)
    for i,p in enumerate(family_phasings):
        phases_kmers_L[kmer_counts_normed.index, i] = [family_probability_cache[(k, p)] for k in kmer_counts_normed.apply(lambda x: tuple(x), axis=1).values]
    print('Done compute likelihood matrix')
    

###########################################################
#################### Saving data ##########################
###########################################################
print("Done computing phasing x k-mer matrix for family!")
print("Saving...")
np.savetxt(OUT_DIR + 'likelihood_matrix_phasings_kmers_fam%03d.tsv' % IDX, phases_kmers_L, delimiter='\t', fmt='%.3f')
print('saved to ', OUT_DIR + 'likelihood_matrix_phasings_kmers_fam%03d.tsv' % IDX)

np.savetxt(OUT_DIR + 'global_regions_phasings_fam%03d.tsv' % IDX, global_regions_phasings_fam, delimiter='\t', fmt='%.0f')
print('saved to ', OUT_DIR +  'global_regions_phasings_fam%03d.tsv' % IDX)
