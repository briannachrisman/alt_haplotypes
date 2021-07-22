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

ml python/3.6
N=$((SLURM_ARRAY_TASK_ID-1))
python3.6 -u $MY_HOME/alt_haplotypes/src/ground_truth/filter_kmers.py $N