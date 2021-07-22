#!/bin/sh
#SBATCH --job-name=localize_ground_truth
#SBATCH --partition=owners
#SBATCH --array=1-11
#SBATCH --output=/scratch/users/briannac/logs/localize_ground_truth_%a.out
#SBATCH --error=/scratch/users/briannac/logs/localize_ground_truth_%a.err
#SBATCH --time=10:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize_ground_truth.sh

N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)


cd $MY_HOME/alt_haplotypes

#if [ ! -f intermediate_files/localize/ground_truth/localized_${N_digits}.txt ]; then
    ml python/3.6.1 
    python3.6 -u src/localize/localize_ground_truth.py $N
#fi

