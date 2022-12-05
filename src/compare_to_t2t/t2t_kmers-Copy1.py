from Bio import SeqIO
import pandas as pd
from collections import Counter
import numpy as np
from tqdm import tqdm
import sys

chrom = int(sys.argv[1])-1
records = [r for r in SeqIO.parse(
    '/home/groups/dpwall/briannac/general_data/reference_genomes/t2t/chm13.draft_v1.1.fasta', 'fasta')]
t2t_kmers = dict()
r = records[chrom]
print(chrom)
seq = r.seq
for loci in tqdm(range(len(r)-100)):
    k = str(seq[loci:(loci+100)])
    if k in t2t_kmers: t2t_kmers[k] = t2t_kmers[k] + [(chrom, loci)]
    else: t2t_kmers[k] = [(chrom, loci)]
            
np.save('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/t2t_comparison/t2t_kmers_%i.npy' % chrom, t2t_kmers)