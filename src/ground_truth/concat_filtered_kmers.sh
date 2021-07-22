#!/bin/sh
#SBATCH --job-name=filter_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/filter_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/filter_kmers.err
#SBATCH --time=0:10:00
#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/ground_truth/filter_kmers.sh
cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/ground_truth/sample_kmer_matrix

cat known_alt_haplotype_kmers_filt.*.tsv > kmers.filt.tsv
cp kmers.filt.tsv  /home/groups/dpwall/briannac/alt_haplotypes/data/known_kmer_counts.tsv
 
\rm known_alt_haplotype_kmers_filt.*.tsv

cat known_alt_haplotype_kmers_filt.*.txt > known_kmers.txt
cp known_kmers.txt  /home/groups/dpwall/briannac/alt_haplotypes/data/known_kmers.txt


\rm known_alt_haplotype_kmers_filt.*.txt