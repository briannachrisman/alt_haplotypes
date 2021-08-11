import pandas as pd
import time 
import sys
import numpy as np
N = int(sys.argv[1])

print("Filtering counts...")
df = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unmapped/query_counts.unmapped_reads.%04d.tsv.gz' % N,
                  usecols=[i for i in range(4569) if i!=3741]) # Weird thing with column 3741 for some reason.
# Somehow 09C82938 has two headings from old bug. Hacky code to delete one of the '09C82938' headings and shift everything upwards.
if df['09C82938'].values[0]=='09C82938':
    bad_col = df['09C82938'].iloc[1:]
    new_df = df.iloc[:-1].copy()
    new_df['09C82938'] = bad_col.values
    df = new_df.astype(int)


df = df[df.sum(axis=1)>0]
df = df[((df>0).mean(axis=1)>.2) & ((df>0).mean(axis=1)<.8)]
df = df[df.apply(lambda x: (np.median(x[x!=0])>2) & (np.median(x[x!=0])<20), axis=1)]
print(len(df), ' kmers')
df.index = N*100000+df.index
print(N,len(df))
df.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unmapped/filt/kmers_unmapped_counts.%04d.tsv' % N, sep='\t', header=None)


print('Filtering k-mers...')
with open('/home/groups/dpwall/briannac/alt_haplotypes/data/unmapped_kmers.txt') as in_file: #intermediate_files/ground_truth/sample_kmer_counts/known_alt_haplotype_kmers.txt') as in_file:
    i=0
    with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unmapped/filt/kmers_unmapped.%04d.txt' % N, 'w') as out_file:
        line = in_file.readline()
        while line:
            if i in df.index:
                out_file.write(line)
            line = in_file.readline()
            i = i + 1

            
# LINES 264492894