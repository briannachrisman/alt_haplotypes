#!/bin/bash
#SBATCH --job-name=concat_family_probability_cache
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_family_probability_cache.out
#SBATCH --error=/scratch/users/briannac/logs/concat_family_probability_cache.err
#SBATCH --time=100:00:00
#SBATCH --mem=700G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/localize/concat_family_probability_cache.sh


ml python/3.6

python3.6 -u $MY_HOME/alt_haplotypes/src/localize/concat_family_probability_cache.py