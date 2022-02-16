#!/bin/sh
#SBATCH --job-name=t2t_kmers
#SBATCH --partition=owners
#SBATCH --array=1-23
#SBATCH --output=/scratch/users/briannac/logs/t2t_kmers_%a.out
#SBATCH --error=/scratch/users/briannac/logs/t2t_kmers_%a.err
#SBATCH --time=10:00:00
#SBATCH --mem=200G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/t2t_kmers.sh

ml python/3.6.1
python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/t2t_kmers.py $SLURM_ARRAY_TASK_ID

