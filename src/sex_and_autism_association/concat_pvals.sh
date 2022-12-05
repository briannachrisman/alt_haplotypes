#!/bin/bash
#SBATCH --job-name=concat_pvals
#SBATCH --partition=dpwall
#SBATCH --array=1
#SBATCH --output=/scratch/users/briannac/logs/concat_pvals.out
#SBATCH --error=/scratch/users/briannac/logs/concat_pvals.err
#SBATCH --time=1:00:00
#SBATCH --mem=100GB
####SBATCH --cpus-per-task=5
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

# file at $MY_HOME/alt_haplotypes/src/sex_and_autism_association/concat_pvals.sh

cd /home/groups/dpwall/briannac/alt_haplotypes/

cat intermediate_files/pvals_asd/pvals_asd_*.tsv > results/autism_and_sex_association/pvals_asd.tsv
#cat intermediate_files/pvals_sex/pvals_sex_*.tsv > results/autism_and_sex_association/pvals_sex.tsv
cat intermediate_files/sig_covs_asd/sig_covs_asd_*.tsv > results/autism_and_sex_association/sig_covs_asd.tsv
#cat intermediate_files/sig_covs_sex/sig_covs_sex_*.tsv > results/autism_and_sex_association/sig_covs_sex.tsv