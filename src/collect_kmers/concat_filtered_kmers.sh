#!/bin/sh
#SBATCH --job-name=concat_filter_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_filter_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/concat_filter_kmers.err
#SBATCH --time=10:00:00
#SBATCH --mem=30G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/collect_kmers/concat_filtered_kmers.sh

cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unmapped/filt
echo "unzipping..."

cat kmers_unmapped_counts.*.tsv > /home/groups/dpwall/briannac/alt_haplotypes/data/kmers_unmapped_prev_and_median_filt_counts.tsv

cat kmers_unmapped.*.txt > /home/groups/dpwall/briannac/alt_haplotypes/data/kmers_unmapped_prev_and_median_filt.txt
