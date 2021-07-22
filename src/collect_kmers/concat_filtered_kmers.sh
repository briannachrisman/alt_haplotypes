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

cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unmapped/filt
echo "unzipping..."

cat kmers_unmapped_counts.15*.tsv > /home/groups/dpwall/briannac/alt_haplotypes/data/kmers_unmapped_counts_filt.tsv

cat kmers_unmapped.15*.txt > /home/groups/dpwall/briannac/alt_haplotypes/data/kmers_unmapped_filt.txt
