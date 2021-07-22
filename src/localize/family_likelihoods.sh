#!/bin/sh
#SBATCH --job-name=family_likelihoods
#SBATCH --partition=owners
#SBATCH --array=1-1000
#SBATCH --output=/scratch/users/briannac/logs/family_likelihoods_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_likelihoods_%a.err
#SBATCH --time=0:30:00
#SBATCH --mem=15G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods.sh

cd $MY_HOME/alt_haplotypes
N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)

#if [  -f intermediate_files/family_likelihoods/ground_truth/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then

    if [ ! -f intermediate_files/family_likelihoods/unmapped/global_regions_phasings_fam${N_digits}.tsv ]; then

        N_KMERS=$(wc -l data/known_kmers.txt | awk '{print $1}') ### CHANGE DEPENDING ON FILE!
        ml python/3.6.1 
        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/unmapped/ \
             data//home/groups/dpwall/briannac/alt_haplotypes/data/unmapped_kmer_counts.tsv $N_KMERS
    fi
#fi

