#!/bin/sh
#SBATCH --job-name=t2t_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_t2t_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/concat_t2t_kmers.err
#SBATCH --time=10:00:00
#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/concat_t2t_kmers.sh

ml python/3.6.1
python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/concat_t2t_kmers.py 

