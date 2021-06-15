#!/bin/bash
#SBATCH --job-name=build_family_probability_cache
#SBATCH --partition=owners
#SBATCH --array=1-250
#SBATCH --output=/scratch/users/briannac/logs/build_family_probability_cache_%a.out
#SBATCH --error=/scratch/users/briannac/logs/build_family_probability_cache_%a.err
#SBATCH --time=2:00:00
#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/localize/build_family_probability_cache.sh

### SLURM_ARRAY_TASK_ID=1 ### REMOVE AFTER TEST

ml python/3.6
N=$((SLURM_ARRAY_TASK_ID-1))
python3.6 -u $MY_HOME/alt_haplotypes/src/localize/build_family_probability_cache.py $N