import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from Bio import SeqIO
from Bio import Seq
import sys
import multiprocessing as mp

from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.metrics.pairwise import pairwise_distances
import time

from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering
import tqdm
from scipy.sparse import lil_matrix


c = int(sys.argv[1]) # chromsome

DE_NOVO_ASSEMBLE_DIR  = '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/de_novo_assemble/'
DE_NOVO_ASSEMBLE_CHROM_DIR  = '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/de_novo_assemble/chr%s/' % (str(c))



# Get chromosome/successfully localized subset of dataframe.
localized = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized.tsv', comment='#')
localized.columns = ['# median_of_nonzeros', 'prevelance', 'chrom_pred', 'start_pred', 'end_pred']
localized.chrom_pred = [np.nan if np.isnan(i) else round(i) for i in localized.chrom_pred ]
localized = localized[~np.isnan(localized.chrom_pred)]
l = localized[localized.chrom_pred==c].sort_values(['start_pred', 'end_pred'])[['start_pred', 'end_pred']]#.iloc[:1000]



# Construct connectivity matrix.
print("Constructuring similarity matrix")
m = lil_matrix(np.zeros((len(l), len(l))))
for i in range(len(l)):
    start = l.iloc[i].start_pred
    for j in range(i,len(l)):
        start2 = l.iloc[j].start_pred
        end2 = l.iloc[j].end_pred
        if (start2 <= start) & (start <=end2):
            m[i,j] = 1
            m[j,i] = 1
        else: break

            
# Finding Optimal number of clusters.
print("Finding optimal number of clusters")
kmax = 100 ### Try 100 clusters per chromosome ???
n_clusters = [c for c in range(2, kmax+1)]

def SillouetteScore(k):
    alg_clusters =AgglomerativeClustering(n_clusters=k, connectivity=m).fit(l)
    labels = alg_clusters.labels_
    return silhouette_score(l, labels, metric = 'euclidean')


pool = mp.Pool(mp.cpu_count())

sil = pool.map(SillouetteScore, n_clusters)


# Compute sillhouette score for each n_clusters.
#for k in tqdm.tqdm(n_clusters):
print(sil)



print('Optimal number of clusters', n_clusters[np.argmax(sil)])
plt.figure()
plt.plot(n_clusters[:len(sil)], sil, '-x')
plt.savefig(DE_NOVO_ASSEMBLE_CHROM_DIR  + 'silouette_score.svg')

# Retrain model with optimal clustering. 
print("Retraining model with optimal clustering...")
alg_clusters = AgglomerativeClustering(n_clusters=n_clusters[np.argmax(sil)], connectivity=m).fit(l)
labels = alg_clusters.labels_
plt.figure()
for ll in set(labels):
    plt.plot(l[labels==ll].start_pred, l[labels==ll].end_pred, '.')
plt.xlabel('Start')
plt.ylabel('End')
plt.savefig(DE_NOVO_ASSEMBLE_CHROM_DIR  + 'cluster_labels.svg')



print("Reading in k-mer sequences")
kmer_seqs = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/kmers_unmapped_prev_and_median_filt.txt', 
                          header=None)
kmer_seqs = kmer_seqs.loc[l.index]
print("Writing fastq files...")
for ll in set(labels):
    print(ll)
    sequences = [SeqIO.SeqRecord(seq = Seq.Seq(seq[0]), id=str(idx)) for idx, seq in kmer_seqs.loc[list(l[labels==ll].index)].iterrows()]
    SeqIO.write(sequences, DE_NOVO_ASSEMBLE_CHROM_DIR + "cluster_%i.fasta" % ll, "fasta")
    print('Written to ', DE_NOVO_ASSEMBLE_CHROM_DIR + "cluster_%i.fasta" % ll)
