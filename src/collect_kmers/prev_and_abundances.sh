#!/bin/bash
#SBATCH --job-name=prev_and_abundances
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/prev_and_abundances.out
#SBATCH --error=/scratch/users/briannac/logs/prev_and_abundances.err
#SBATCH --time=60:00:00
#SBATCH --mem=200GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu


### file at $MY_HOME/alt_haplotypes/src/collect_kmers/prev_and_abundances.sh
ml python/3.6.1

\rm /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_abundances.txt
\rm /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_prevs.txt
python3.6 -u $MY_HOME/alt_haplotypes/src/collect_kmers/prev_and_abundances.py 
