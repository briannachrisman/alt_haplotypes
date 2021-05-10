#!/bin/sh
#SBATCH --job-name=family_regions_to_global_regions
#SBATCH --partition=owners
#SBATCH --array=1-22
#SBATCH --output=/scratch/users/briannac/logs/family_regions_to_global_regions_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_regions_to_global_regions_%a.err
#SBATCH --time=1:00:00
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.sh

python3 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.py $SLURM_ARRAY_TASK_ID

if [[ "$SLURM_ARRAY_TASK_ID" -eq 22 ]]; then
    python3 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.py X
fi