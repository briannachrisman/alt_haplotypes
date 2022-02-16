#!/bin/sh
#SBATCH --job-name=localize_decoy
#SBATCH --partition=owners
#SBATCH --array=1-110
#SBATCH --output=/scratch/users/briannac/logs/localize_decoy_%a.out
#SBATCH --error=/scratch/users/briannac/logs/localize_decoy_%a.err
#SBATCH --time=4:00:00
#SBATCH --mem=70G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize.sh

# Note: Change to fit however many sequences we are trying to localize / 100000

ml python/3.6.1 

N=$((SLURM_ARRAY_TASK_ID))
N_digits=$(printf "%03d" $N)

cd $MY_HOME/alt_haplotypes

#python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/synthetic_data1/ intermediate_files/localize/synthetic_data1/ 10000


#python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/synthetic_data10/ intermediate_files/localize/synthetic_data10/ 101000


#python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/synthetic_data100/ intermediate_files/localize/synthetic_data100/ 101000



python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/decoy_known/ intermediate_files/localize/decoy_known/ 10000
# This should be array 1-110