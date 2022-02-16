#!/bin/bash
#SBATCH --job-name=autism_and_sex_association
#SBATCH --partition=dpwall
#SBATCH --array=4,6,92,104,105,106,113,114,121,122,123,124,125,131,132,134,137,138,139,140,141,142,144,145,147,148,149,150,151,152,154,156,157,158
#SBATCH --output=/scratch/users/briannac/logs/autism_and_sex_association_%a.out
#SBATCH --error=/scratch/users/briannac/logs/autism_and_sex_association_%a.err
#SBATCH --time=20:00:00
#SBATCH --mem=5GB
####SBATCH --cpus-per-task=5
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

# file at $MY_HOME/alt_haplotypes/src/sex_and_autism_association/autism_and_sex_association.sh


ml python/3.6.1


for I_TO_ADD in 0
do
    N=$((SLURM_ARRAY_TASK_ID + I_TO_ADD - 1))
    echo $N
    python3 -u $MY_HOME/alt_haplotypes/src/sex_and_autism_association/autism_and_sex_association.py $N
done
