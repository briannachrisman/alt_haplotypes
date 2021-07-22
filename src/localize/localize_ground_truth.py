import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import sys

idx_to_global_region = np.load('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/idx_to_global_region.npy', allow_pickle=True).item()


N = int(sys.argv[1])
n_rows = 100000
max_chunk = 1000
nth_start = N*n_rows


LIKELIHOOD_FILE_DIR = '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/ground_truth/'
LOCALIZED_FILE_DIR = '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/ground_truth/'

print("Loading regions....")
regions = np.loadtxt(LIKELIHOOD_FILE_DIR + 'global_regions_phasings.tsv', delimiter='\t')
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
    if len(np.where(L>=thresh)[0])==0: return (np.nan, np.nan, np.nan)
    start = np.where(L>=thresh)[0][0]
    end = np.where(L>=thresh)[0][-1]
    start = idx_to_global_region[start]
    end = idx_to_global_region[end]
    start_chr = int(start.split('.')[0].replace('chr', '').replace('X', '23').replace('Y', '24'))
    end_chr = int(end.split('.')[0].replace('chr', '').replace('X', '23').replace('Y', '24'))
    start_loci = int(start.split('.')[1])
    end_loci = int(end.split('.')[-1])
    if start_chr!=end_chr: return (np.nan, np.nan, np.nan)
    return (start_chr, start_loci, end_loci)

stds = [.05, .1, .15, .2, .25, .5, 1]
full_df = np.zeros((n_rows,3*len(stds) + 4))
for start in np.arange(nth_start,nth_start + n_rows, max_chunk):
    
    print('Loading likelihoods...')
    L = np.loadtxt(LIKELIHOOD_FILE_DIR + 'likelihood_matrix_phasings_kmers.tsv' ,
                  delimiter='\t',max_rows=max_chunk, skiprows=start)
    print("Matrix multiplication...")
    
    
    kmer_counts = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/data/known_kmer_counts.tsv',
                            header=None, index_col=0, nrows=max_chunk,skiprows=start)

    kmer_names = pd.read_table(
        '/home/groups/dpwall/briannac/alt_haplotypes/data/known_kmers.txt',
    sep='\t', header=None, nrows=max_chunk, skiprows=start)
    
    
    localized_regions = dict()
    likelihoods = np.matmul(L, regions_t)
    start_idx =  start-nth_start

    for i, std in enumerate(stds):
        idx = 4 + 3*i
        full_df[start_idx:(start_idx+len(L)),idx:(idx+3)] = [GlobalInterval(l,std)  for l in likelihoods] #[np.array(l) for l in localized_regions]


    # Ground truth values.
    kmer_chrom = [int(c.split('_')[0].replace('chr', '').replace('X', '23').replace('Y', '24')) for c in kmer_names[1]]
    kmer_loci = [int(c.split(':')[1].split('-')[0]) + l for c,l in zip(kmer_names[2], kmer_names[3])]
    full_df[start_idx:(start_idx+len(L)),0] = [int(c.split('_')[0].replace('chr', '').replace('X', '23').replace('Y', '24')) for c in kmer_names[1]]
    full_df[start_idx:(start_idx+len(L)),1] = [int(c.split(':')[1].split('-')[0]) + l for c,l in zip(kmer_names[2], kmer_names[3])]

    # Some metrics about the ground truth kmers.
    full_df[start_idx:(start_idx+len(L)),2] = kmer_counts.apply(axis=1, func=lambda x: round(x[x!=0].median(), 1))
    full_df[start_idx:(start_idx+len(L)),3] = np.round((kmer_counts>0).mean(axis=1), 3)


    
    if len(L) < max_chunk: break
    
header = ['chrom_true', 'loci_true', 'median_of_nonzeros', 'prevalence']
for std in stds:
    header = header + ['chrom_pred_%s' % str(std), 'start_pred_%s' % str(std), 'end_pred_%s' % str(std)]
    
np.savetxt(LOCALIZED_FILE_DIR + 'localized_%03d.txt' % N , np.array(full_df),
           header='\t'.join(header), delimiter='\t')
print('saved to ', LOCALIZED_FILE_DIR + ('localized_%03d.txt' % N))