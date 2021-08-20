#!/bin/sh
#SBATCH --job-name=localize_unmapped
#SBATCH --partition=dpwall
#SBATCH --array=1
#SBATCH --output=/scratch/users/briannac/logs/localize_unmapped.out
#SBATCH --error=/scratch/users/briannac/logs/localize_unmapped.err
#SBATCH --time=1:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 5679230 kmers (so 57 100,000-kmer regions) total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize_unmapped.sh

# 5 million 
ml python/3.6.1 

N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)

cd $MY_HOME/alt_haplotypes

python3.6 -u src/localize/localize_unmapped.py $N

