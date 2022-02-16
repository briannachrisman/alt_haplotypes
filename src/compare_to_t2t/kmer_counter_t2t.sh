#!/bin/sh
#SBATCH --job-name=kmer_counter_t2t
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/kmer_counter_t2t.out
#SBATCH --error=/scratch/users/briannac/logs/kmer_counter_t2t.err
#SBATCH --time=20:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total -- 727 should actually work.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods.sh



cd $MY_HOME/alt_haplotypes/intermediate_files/t2t_comparison

jellyfish count -m 100 -s 100M -C -o  t2t_kmers.jf /home/groups/dpwall/briannac/general_data/reference_genomes/t2t/chm13.draft_v1.1.fasta 

cat $MY_HOME/alt_haplotypes/data/kmers_unmapped_prev_and_median_filt.txt  | xargs jellyfish query t2t_kmers.jf  | awk  '{print $2}' > kmer_counts.txt