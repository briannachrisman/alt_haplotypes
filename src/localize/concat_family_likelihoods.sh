#!/bin/sh
#SBATCH --job-name=concat_family_likelihoods
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/concat_family_likelihoods.out
#SBATCH --error=/scratch/users/briannac/logs/concat_family_likelihoods.err
#SBATCH --time=15:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu


### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/concat_family_likelihoods.sh


cd $MY_HOME/alt_haplotypes/intermediate_files/family_likelihoods/unmapped

\rm global_regions_phasings.tsv
paste global_regions_phasings_fam*.tsv > global_regions_phasings.tsv


echo "pasting likelihood"

\rm likelihood_matrix_phasings_kmers.tsv
paste likelihood_matrix_phasings_kmers_fam*.tsv > likelihood_matrix_phasings_kmers.tsv

#\rm likelihood_matrix_phasings_kmers_fam*.tsv
#\rm global_regions_phasings_fam*.tsv 