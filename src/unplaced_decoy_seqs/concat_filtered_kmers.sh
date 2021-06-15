#!/bin/sh
#SBATCH --job-name=filter_kmers
#SBATCH --partition=owners
#SBATCH --array=1-511
#SBATCH --output=/scratch/users/briannac/logs/filter_kmers_%a.out
#SBATCH --error=/scratch/users/briannac/logs/filter_kmers_%a.err
#SBATCH --time=0:10:00
#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/ground_truth/filter_kmers.sh
cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/ground_truth/sample_kmer_matrix

cat kmers.filt.*.tsv > kmers.filt.tsv
 
\rm kmers.filt.*.tsv

cat known_alt_haplotype_kmers_filt.*.txt > known_alt_haplotype_kmers_filt.txt


\rm known_alt_haplotype_kmers_filt.*.txt