#!/bin/sh
#SBATCH --job-name=localize_unmapped
#SBATCH --partition=owners
#SBATCH --array=47,49
#SBATCH --output=/scratch/users/briannac/logs/localize_unmapped_%a.out
#SBATCH --error=/scratch/users/briannac/logs/localize_unmapped_%a.err
#SBATCH --time=48:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 5679230 kmers (so 57 100,000-kmer regions) total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize_unmapped.sh

ml python/3.6.1 

N=$((SLURM_ARRAY_TASK_ID))
N_digits=$(printf "%03d" $N)

cd $MY_HOME/alt_haplotypes

python3.6 -u src/localize/localize_unmapped.py $N

