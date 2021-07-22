#!/bin/sh
#SBATCH --job-name=concat_region_approximations
#SBATCH --partition=owners
#SBATCH --output=/scratch/users/briannac/logs/concat_region_approximations.out
#SBATCH --error=/scratch/users/briannac/logs/concat_region_approximations.err
#SBATCH --time=2:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/concat_region_approximations.sh


cd $MY_HOME/alt_haplotypes

cat intermediate_files/localize/ground_truth/localized_*.txt > $MY_HOME/alt_haplotypes/results/approximate_regions/localized_ground_truth.tsv

#\rm intermediate_files/approximate_regions/ground_truth_approximate_region_*.txt


#cat intermediate_files/localize/ground_truth/localized_000.txt intermediate_files/localize/ground_truth/localized_001.txt intermediate_files/localize/ground_truth/localized_002.txt intermediate_files/localize/ground_truth/localized_003.txt > $MY_HOME/alt_haplotypes/results/approximate_regions/localized_ground_truth.tsv
