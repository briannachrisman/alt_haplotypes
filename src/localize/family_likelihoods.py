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
from multiprocessing import Pool, freeze_support, cpu_count
import os


# Set up file locations.
IDX = int(sys.argv[1])
OUT_DIR = sys.argv[2] # /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/ground_truth/
KMER_COUNTS_FILE = sys.argv[3] #'/home/groups/dpwall/briannac/alt_haplotypes/data/known_kmer_counts.tsv'
N_KMERS = int(sys.argv[4]) #1094247 # Number of kmers in KMER_COUNTS_FILE file
N_CPUS=30

PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/'
BAM_MAPPINGS_FILE = '/home/groups/dpwall/briannac/general_data/bam_mappings.csv'


###################################################################
#################### Loading files. ##############################
###################################################################
print("Loading in files...")
# Load in family region/global region conversion data.
fam_region_to_idx = np.load(PHASINGS_DIR +  'fam_region_to_idx.npy', allow_pickle=True).item()
global_region_to_idx = np.load(PHASINGS_DIR +  'global_region_to_idx.npy', allow_pickle=True).item()
fam_idx_to_global_idx = np.load(PHASINGS_DIR + 'fam_regions_to_global_regions.npy', allow_pickle=True)
family_info = pd.read_pickle(PHASINGS_DIR + 'fam_list.df')

# Info from BAM mappings.
bam_mappings = pd.read_csv(BAM_MAPPINGS_FILE, sep='\t', index_col=1)
bam_mappings = bam_mappings[bam_mappings['status']=='Passed_QC_analysis_ready']

# This sample is messed up in the unmapped reads, 
if 'unmapped' in KMER_COUNTS_FILE:
    bam_mappings = bam_mappings.drop('09C86428')

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
max_count = 40
eps = 1e-20
possible_repeats = {0,1,2,3,4,5}
with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'rb') as f:
    phased_fam_dict = pickle.load(f)
family_phasings = sorted(list(set([tuple(v) for v in phased_fam_dict[family].values])))
poisson_cache = {}
avg_kmer_depth=np.mean(list(kmer_depth_dict.values()))
for i in (possible_repeats):
    for j in possible_repeats:
        if j>i: 
            for k in range(max_count):
                prob = poisson.pmf(k=k, mu=int(i+j)*avg_kmer_depth)
                if prob>eps: poisson_cache[(i+j, k)] = prob
    
def cached_poisson_pmf(k,g):
    if (g==0) & (k!=0): return eps
    if (g==0) & (k==0): return 1-3*eps
    if (g,k) not in poisson_cache: return eps
    return min(max(poisson_cache[g,k], eps), 1-3*eps)

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
# If we didn't do this, we would end up with have the log-likelihood=0 at regions w/unknown phases, this will give unknown regions an unfair advantage.
impute_vector = np.zeros(len(family_phasings))
impute_vector[np.argmax(global_regions_phasings_fam.sum(axis=0))] = 1

#impute_vector = np.apply_along_axis(arr=global_regions_phasings_fam[np.where(global_regions_phasings_fam.sum(axis=1)!=0)[0], :], func1d=np.median, axis=0)
for i in np.where(global_regions_phasings_fam.sum(axis=1)==0)[0]:
    global_regions_phasings_fam[i,:]=impute_vector
 

print("Computing phasing x k-mer region likelihood matrix...")
phases_kmers_L = np.zeros((N_KMERS,len(family_phasings)))  # Initialize likelihood matrix (phases as rows, kmers as columns)

# Read in kmer counts file. (Hacky way to fix some differences between unmapped reads & synthetic datasets.)
if 'unmapped' in KMER_COUNTS_FILE: # Unmappd data has no header.
    chunks = pd.read_table(KMER_COUNTS_FILE, header=None,  chunksize=10000000, usecols=1+cols_in_df, nrows=N_KMERS)
elif 'decoy' in KMER_COUNTS_FILE: # Decoy data has no header.
    chunks = pd.read_table(KMER_COUNTS_FILE, header=None,  chunksize=100000, usecols=1+cols_in_df, nrows=N_KMERS)
else: # synthetic dataset has header with samples.
    chunks = pd.read_table(KMER_COUNTS_FILE, chunksize=100000, nrows=N_KMERS,usecols=samples)    

# Faster way to take product + max L.    
def prob_product(k_cs, k_m, k_p, phases_ch_compute,possible_gs_mom,possible_gs_dad):
    max_so_far = 0
    for g_m in possible_gs_mom:
        for g_p in iter(possible_gs_dad):
            A = cached_poisson_pmf(k_m,sum(g_m))*cached_poisson_pmf(k_p,sum(g_p))
            for k_c, phase_ch in zip(iter(k_cs), iter(phases_ch_compute)):
                if A <= max_so_far: break
                A=A*cached_poisson_pmf(k_c, g_m[phase_ch[0]]+g_p[phase_ch[1]])
            max_so_far = max(A,max_so_far)
    return max_so_far
    
    
for kmer_counts in chunks:
    if ('unmapped' in KMER_COUNTS_FILE) or ('decoy' in KMER_COUNTS_FILE):
        kmer_counts = kmer_counts[1+cols_in_df]
        kmer_counts.columns = samples
    print(len(kmer_counts), 'kmer counts')
    norm_mult = np.array([avg_k_depth/kmer_depth_dict[c] for c in kmer_counts.columns])
    kmer_counts = kmer_counts[((kmer_counts).sum(axis=1)>0)]
    kmer_counts_normed = kmer_counts.apply(lambda x: x*norm_mult, axis=1)
    kmer_counts_normed = kmer_counts_normed.apply(lambda x: np.round(x/(10**np.floor(np.log10(max(x[x>0]))))), axis=1).astype(int)
    kmer_counts_normed = kmer_counts_normed.applymap(lambda x: min(x,max_count))
    poss_kmer_counts = set([tuple(v) for v in kmer_counts_normed.values])
    family_probability_cache = dict()
    print(len(poss_kmer_counts), 'unique kmer counts')
    for phases_ch in tqdm(family_phasings):
        # If X chromosome:
        if (max([f for ff in phases_ch for f in ff]) > 3) & (max([f for ff in phases_ch for f in ff]) < 8):
            phases_ch_compute = [(f-4,g-4) for f,g in phases_ch]
            possible_gs_mom = [(mat_gt,pat_gt) for mat_gt in possible_repeats for pat_gt in possible_repeats] # Include possible repeats!
            possible_gs_dad = [(mat_gt,0) for mat_gt in possible_repeats]

        # If Y chromosome:
        elif (max([f for ff in phases_ch for f in ff]) > 7):
            phases_ch_compute = [(f-8,g-8) for f,g in phases_ch]
            possible_gs_mom = [(0,0)] 
            possible_gs_dad = [(0,pat_gt) for pat_gt in possible_repeats]

            
        # Autosome or PAR
        else :
            possible_gs_mom = [(mat_gt,pat_gt) for mat_gt in possible_repeats for pat_gt in possible_repeats] 
            possible_gs_dad = [(mat_gt,pat_gt) for mat_gt in possible_repeats for pat_gt in possible_repeats] 
            phases_ch_compute =  phases_ch
        
        # Parallelize this step.
        def myfunc(kmer_count_set):
            k_m = kmer_count_set[0]
            k_p = kmer_count_set[1]
            k_cs = kmer_count_set[2:]
            return ((k_m, k_p, *k_cs), round(np.log2(prob_product(k_cs, k_m, k_p, phases_ch_compute,iter(possible_gs_mom),possible_gs_dad)),3))

        pool = Pool(N_CPUS)
        family_probability_cache.update({(k, phases_ch):v for k,v in pool.map(myfunc,poss_kmer_counts)})
        pool.close()
        pool.join()
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
