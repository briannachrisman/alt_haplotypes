#!/bin/sh
#SBATCH --job-name=family_regions_to_global_regions
#SBATCH --partition=dpwall
#SBATCH --array=1-24
#SBATCH --output=/scratch/users/briannac/logs/family_regions_to_global_regions_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_regions_to_global_regions_%a.err
#SBATCH --time=0:10:00
#SBATCH --mem=1GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.sh


ml python/3.6


if [[ "$SLURM_ARRAY_TASK_ID" -eq 23 ]]; then
    python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.py XX
fi

if [[ "$SLURM_ARRAY_TASK_ID" -eq 24 ]]; then
    python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.py YY
fi

N=$(printf "%02g" $SLURM_ARRAY_TASK_ID)
python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/family_regions_to_global_regions.py $N