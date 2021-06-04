#!/bin/sh
#SBATCH --job-name=list_of_global_and_family_regions
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/list_of_global_and_family_regions.out
#SBATCH --error=/scratch/users/briannac/logs/list_of_global_and_family_regions.err
#SBATCH --time=0:30:00
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/list_of_global_and_family_regions.sh

ml python/3.6
python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/list_of_global_and_family_regions.py
