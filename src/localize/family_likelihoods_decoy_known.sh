#!/bin/sh
#SBATCH --job-name=family_likelihoods_decoy_known
#SBATCH --partition=dpwall
#SBATCH --array=10,107,124,134,174,178,19,199,213,223,249,268,294,30,344,348,370,376,40,408,415,426,438,443,471,476,482,490,503,518,529,549,560,564,575,581,588,608,609,61,627,654,718,76,764,778,83,99
#SBATCH --output=/scratch/users/briannac/logs/family_likelihoods_decoy_known_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_likelihoods_decoy_known_%a.err
#SBATCH --time=144:00:00
#SBATCH --mem=20G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total -- 727 should actually work.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods_decoy_known.sh

# # SLURM_ARRAY_TASK_ID=1 ### COMMENT OUT WHEN RUNNING BATCH.

cd $MY_HOME/alt_haplotypes
N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)
N_KMERS=1094247 # Number of k-mers/counts present in file.



ml python/3.6.1

if [ ! -f intermediate_files/family_likelihoods/decoy_known/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then
        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/decoy_known/ \
             intermediate_files/counts/decoy_known.tsv $N_KMERS
fi
