from Bio import SeqIO
import pandas as pd
from collections import Counter
import numpy as np
from tqdm import tqdm
import sys


full_dict = np.load('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/t2t_comparison/t2t_kmers_0.npy', allow_pickle=True)

for i in range(1,23):
    print(i)
    kmer_dict = np.load('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/t2t_comparison/t2t_kmers_%i.npy' % chrom, allow_pickle=True)
    for k in kmer_dict:
        if k in full_dict: full_dict[k] = full_dict[k] + kmer_dict[k]
        else: full_dict[k] = kmer_dict[k]

print('saving...')
np.save('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/t2t_comparison/t2t_kmers_full.npy', full_dict)