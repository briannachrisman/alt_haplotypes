#!/bin/sh
#SBATCH --job-name=family_likelihoods_synthetic_dataset
#SBATCH --partition=owners
#SBATCH --array=10,100,102,107,108,121,124,134,154,16,160,174,176,178,186,19,194,199,223,225,231,238,244,249,255,262,268,274,286,294,30,302,308,311,318,321,324,327,333,348,356,370,376,377,383,385,399,4,40,408,412,415,422,426,431,438,440,443,452,458,469,47,471,474,476,478,482,490,496,503,505,512,518,52,525,545,549,560,564,572,575,58,581,588,591,608,61,625,627,629,634,650,654,665,676,692,695,700,710,718,723,727,730,732,749,755,76,764,768,770,774,779,784,794,799,801,803,806,815,819,821,823,825,828,83,836,840,842,855,857,860,863,867,870,91,94,99
#SBATCH --output=/scratch/users/briannac/logs/family_likelihoods_synthetic_dataset_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_likelihoods_synthetic_dataset_%a.err
#SBATCH --time=40:00:00
#SBATCH --mem=20G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total -- 727 should actually work.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods_synthetic_dataset.sh

## SLURM_ARRAY_TASK_ID=2 ### COMMENT OUT WHEN RUNNING BATCH.

cd $MY_HOME/alt_haplotypes
N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)
N_KMERS=101000 # Number of k-mers/counts present in file.



ml python/3.6.1

# Synthetic dataset ~1 repeat
if [ ! -f intermediate_files/family_likelihoods/synthetic_data1/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then
        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/synthetic_data1/ \
             intermediate_files/counts/synthetic_data_1_repeats_all.tsv $N_KMERS
fi

# Synthetic dataset ~10 repeat
#if [ ! -f intermediate_files/family_likelihoods/synthetic_data10/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then   
#        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/synthetic_data10/ \
#             intermediate_files/counts/synthetic_data_10_repeats_all.tsv $N_KMERS
#fi
    

# Synthetic dataset ~100 repeat
#if [ ! -f intermediate_files/family_likelihoods/synthetic_data100/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then
#        ml python/3.6.1 
#        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/synthetic_data100/ \
#             intermediate_files/counts/synthetic_data_100_repeats_all.tsv $N_KMERS
#fi
