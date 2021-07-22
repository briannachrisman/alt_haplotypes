#!/bin/sh
#SBATCH --job-name=localize_unknown_decoys
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/localize_unknown_decoys.out
#SBATCH --error=/scratch/users/briannac/logs/localize_unknown_decoys.err
#SBATCH --time=1:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize_unknown_decoys.sh

ml python/3.6.1 

N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)

cd $MY_HOME/alt_haplotypes

python3.6 -u src/localize/localize_unmapped.py $N

