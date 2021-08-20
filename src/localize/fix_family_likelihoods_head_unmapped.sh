#!/bin/sh
#SBATCH --job-name=family_likelihoods
#SBATCH --partition=owners
#SBATCH --array=10
#SBATCH --output=/scratch/users/briannac/logs/family_likelihoods_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_likelihoods_%a.err
#SBATCH --time=40:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total -- 727 should actually work.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods.sh

cd $MY_HOME/alt_haplotypes/intermediate_files/family_likelihoods/unmapped
for lfile in likelihood_matrix_phasings_kmers_fam*.tsv; do
    echo $lfile
    mv $lfile $lfile.tmp
    head -n 5679230 $lfile.tmp > $lfile
    #\rm $lfile.tmp
done


