#!/bin/sh
#SBATCH --job-name=concat_filter_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_filter_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/concat_filter_kmers.err
#SBATCH --time=1:00:00
#SBATCH --mem=30G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/unplaced_decoy_seqs/concat_filter_kmers.sh
cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix

cat kmers.filt.*.tsv > kmers.filt.tsv
mv kmers.filt.tsv  /home/groups/dpwall/briannac/alt_haplotypes/data/unplaced_decoy_seqs_kmer_counts.tsv
 
#\rm kmers.filt.*.tsv

cat unknown_alt_haplotype_kmers_filt.*.txt > unknown_kmers.txt
mv unknown_kmers.txt  /home/groups/dpwall/briannac/alt_haplotypes/data/unplaced_decoy_seqs_kmers.txt


#\rm unknown_alt_haplotype_kmers_filt.*.txt