import pandas as pd
import time 
import sys

N = int(sys.argv[1])

print("Filtering counts...")
df = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/ground_truth/sample_kmer_matrix/kmers.%03d.tsv.gz' % N)
df = df[df.sum(axis=1)>0]
df.index = N*100000+df.index
print(N,len(df))
df.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/ground_truth/sample_kmer_matrix/kmers.filt.%03d.tsv' % N, sep='\t', header=None)


print('Filtering k-mers...')
with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/ground_truth/sample_kmer_counts/known_alt_haplotype_kmers.txt') as in_file:
    i=0
    with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/ground_truth/sample_kmer_matrix/known_alt_haplotype_kmers_filt.%03d.txt' % N, 'w') as out_file:
        line = in_file.readline()
        while line:
            if i in df.index:
                out_file.write(line)
            line = in_file.readline()
            i = i + 1
