#!/bin/sh
#SBATCH --job-name=concat_region_approximations
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_region_approximations.out
#SBATCH --error=/scratch/users/briannac/logs/concat_region_approximations.err
#SBATCH --time=100:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/concat_region_approximations.sh


cd $MY_HOME/alt_haplotypes

cat intermediate_files/localize/unmapped/localized_*.tsv >  intermediate_files/localize/unmapped/localized.tsv
cp intermediate_files/localize/unmapped/localized.tsv $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped.tsv

cat intermediate_files/localize/unmapped/localized_*_start.bed >  intermediate_files/localize/unmapped/localized_start.bed
cp intermediate_files/localize/unmapped/localized_start.bed $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped_start.bed

cat intermediate_files/localize/unmapped/localized_*_start_with_Y.bed >  intermediate_files/localize/unmapped/localized_start_with_Y.bed
cp intermediate_files/localize/unmapped/localized_start_with_Y.bed $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped_start_with_Y.bed


cat intermediate_files/localize/unmapped/localized_*_end.bed >  intermediate_files/localize/unmapped/localized_end.bed
cp intermediate_files/localize/unmapped/localized_end.bed $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped_end.bed

cat intermediate_files/localize/unmapped/localized_*_end_with_Y.bed >  intermediate_files/localize/unmapped/localized_end_with_Y.bed
cp intermediate_files/localize/unmapped/localized_end_with_Y.bed $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped_end_with_Y.bed


cat intermediate_files/localize/unmapped/localized_*_T2T_start.bed >  intermediate_files/localize/unmapped/localized_T2T_start.bed
cp intermediate_files/localize/unmapped/localized_T2T_start.bed $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped_T2T_start.bed

cat intermediate_files/localize/unmapped/localized_*_T2T_end.bed >  intermediate_files/localize/unmapped/localized_T2T_end.bed
cp intermediate_files/localize/unmapped/localized_T2T_end.bed $MY_HOME/alt_haplotypes/results/approximate_regions/localized_unmapped_T2T_end.bed




#\rm intermediate_files/approximate_regions/ground_truth_approximate_region_*.txt


#cat intermediate_files/localize/ground_truth/localized_000.txt intermediate_files/localize/ground_truth/localized_001.txt intermediate_files/localize/ground_truth/localized_002.txt intermediate_files/localize/ground_truth/localized_003.txt > $MY_HOME/alt_haplotypes/results/approximate_regions/localized_ground_truth.tsv
