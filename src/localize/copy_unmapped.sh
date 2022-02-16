#!/bin/sh
#SBATCH --job-name=copy_unmapped
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/copy_unmapped.out
#SBATCH --error=/scratch/users/briannac/logs/copy_unmapped.err
#SBATCH --time=60:00:00
#SBATCH --mem=20G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu


### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/copy_unmapped.sh


cd $MY_HOME/alt_haplotypes
cp data/kmers_unmapped_counts_filt.tsv intermediate_files/counts/unmapped_filt.tsv