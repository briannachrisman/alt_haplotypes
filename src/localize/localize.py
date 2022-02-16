# File at $MY_HOME/alt_haplotypes/src/localize/localize_unknown_decoys.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import sys


N = int(sys.argv[1])-1
LIKELIHOOD_FILE_DIR = sys.argv[2] #'/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/unmapped_with_sex/'
LOCALIZED_FILE_DIR = sys.argv[3] #'/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped_with_sex/'
n_rows = int(sys.argv[4])

print(LIKELIHOOD_FILE_DIR + 'likelihood_matrix_phasings_kmers.tsv')

idx_to_global_region = np.load('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/idx_to_global_region.npy', allow_pickle=True).item()


max_chunk = 1000
nth_start = N*n_rows


print("Loading regions....")
regions = np.loadtxt(LIKELIHOOD_FILE_DIR + 'global_regions_phasings.tsv', delimiter='\t')
#regions = np.loadtxt('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/global_regions_phasings/global_regions_phasings.tsv', 
#                     delimiter='\t')

regions_t = regions.transpose()


def GlobalInterval(L, std_thresh=1):
    '''
        Returns the the smallest and largest position where the likelihood is <=1 standard deivation away from the maximum likelihood.
                Parameters:
                        L (array): Array of likelihoods for each global genomic region.
                        std_thresh (float): Number of standard deviations away from the maximum likelihood to consider.

                Returns:
                        interval (tuple): The start and end idxs.
        '''    
    thresh = np.max(L) - std_thresh*np.std(L)
    if len(np.where(L>thresh)[0])==0: return (np.nan, np.nan, np.nan)
    start = np.where(L>thresh)[0][0]
    end = np.where(L>thresh)[0][-1]
    start = idx_to_global_region[start]
    end = idx_to_global_region[end]
    start_chr = int(start.split('.')[0].replace('chr', '').replace('XX', '23').replace('YY', '24'))
    end_chr = int(end.split('.')[0].replace('chr', '').replace('XX', '23').replace('YY', '24'))
    start_loci = int(start.split('.')[1])
    end_loci = int(end.split('.')[-1])
    if start_chr!=end_chr: return (np.nan, np.nan, np.nan)
    return (start_chr, start_loci, end_loci)


full_df = np.zeros((n_rows,18)) + np.nan


for L in pd.read_table(LIKELIHOOD_FILE_DIR + 'likelihood_matrix_phasings_kmers.tsv' ,
                  chunksize=max_chunk, skiprows=nth_start, header=None, nrows=n_rows): #np.arange(nth_start,nth_start + n_rows, max_chunk):
    
    start = nth_start + L.index[0]
    print(start)
    print('Loading likelihoods...')
    L = np.matrix(L) 
    print("Matrix multiplication...")
    L[np.isinf(L)] = L[~np.isinf(L)].min()

    likelihoods = np.array(np.matmul(L, regions_t))
    localized_regions_1 = [GlobalInterval(l,.01)  for l in likelihoods]
    localized_regions_5 = [GlobalInterval(l,.05)  for l in likelihoods]
    localized_regions_10 = [GlobalInterval(l,.1)  for l in likelihoods]
    localized_regions_25 = [GlobalInterval(l,.25)  for l in likelihoods]
    localized_regions_50 = [GlobalInterval(l,.5)  for l in likelihoods]
    localized_regions_100 = [GlobalInterval(l,1)  for l in likelihoods]

    start_idx =  start-nth_start

    # Our predicted region.
    full_df[start_idx:(start_idx+len(L)),:3] = localized_regions_1 #[np.array(l) for l in localized_regions]
    full_df[start_idx:(start_idx+len(L)),3:6] = localized_regions_5 #[np.array(l) for l in localized_regions]
    full_df[start_idx:(start_idx+len(L)),6:9] = localized_regions_10 #[np.array(l) for l in localized_regions]
    full_df[start_idx:(start_idx+len(L)),9:12] = localized_regions_25 #[np.array(l) for l in localized_regions]
    full_df[start_idx:(start_idx+len(L)),12:15] = localized_regions_50 #[np.array(l) for l in localized_regions]
    full_df[start_idx:(start_idx+len(L)),15:18] = localized_regions_100 #[np.array(l) for l in localized_regions]

    
    if len(L) < max_chunk: break # finish after we can't quite fill up max chunk size.
        
full_df = full_df[:(start_idx + len(L))]
np.savetxt(LOCALIZED_FILE_DIR + 'localized_%03d.tsv' % N , np.array(full_df),
           header='\t'.join(['chrom_pred1', 'start_pred1', 'end_pred1', 
                            'chrom_pred5', 'start_pred5', 'end_pred5',
                            'chrom_pred10', 'start_pred10', 'end_pred10',
                            'chrom_pred25', 'start_pred25', 'end_pred25',
                            'chrom_pred50', 'start_pred50', 'end_pred50',
                            'chrom_pred100', 'start_pred100', 'end_pred100']), delimiter='\t')
    
    
