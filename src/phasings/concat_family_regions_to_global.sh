#!/bin/sh
#SBATCH --job-name=concat_family_regions_to_global
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_family_regions_to_global.out
#SBATCH --error=/scratch/users/briannac/logs/concat_family_regions_to_global.err
#SBATCH --time=0:10:00
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/concat_family_regions_to_global.sh

python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/concat_family_regions_to_global.py 