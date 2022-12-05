import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import sys
import seaborn as sns
import matplotlib.ticker as mtick

if False:
    print('decoy,...')
    prev = np.array([0.0 for i in range(1094247)])
    abundances = np.array([0.0 for i in range(1094247)])
    kmers = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/decoy_known.tsv',  header=None, chunksize=10000, index_col=0)
    i = 0
    for k in kmers:
        print(i)
        prev[i:(i+len(k))] = (k>0).mean(axis=1).values
        abundances[i:(i+len(k))] = k.apply(lambda x: np.median(x[x!=0]),axis=1).values
        i = i + len(k)
    np.savetxt('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/decoy_known_prevs.txt', prev, fmt='%.03f')
    np.savetxt('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/decoy_known_abundances.txt', abundances)

print('unmapped...')
#prev = np.array([0.0 for i in range(104565782)])
#abundances = np.array([0.0 for i in range(104565782)])
kmers = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped.tsv',  header=None, chunksize=10000, index_col=0,nrows=104565782)
i = 0
for k in kmers:
    #if i >= 100000: break
    #print(len(k))
    #print(len((k>0).mean(axis=1).values))
    #print(len(prev[i:(i+len(k))]))
    #print(i)
    with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_prevs.txt', 'a') as f:
        for kk in (k>0).mean(axis=1).values:
            f.write('%.03f\n' % kk)
    with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_abundances.txt', 'a') as f:
        for kk in k.apply(lambda x: np.median(x[x!=0]),axis=1).values:
            f.write('%.01f\n' % kk)
   # i = i + len(k)
#np.savetxt('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_prevs.txt', prev, fmt='%.03f')
#np.savetxt('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_abundances.txt', abundances)