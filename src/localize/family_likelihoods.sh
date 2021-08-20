#!/bin/sh
#SBATCH --job-name=family_likelihoods
#SBATCH --partition=owners
#SBATCH --array=10,19,30,40,61,76,83,99,107,124,134,199,223,249,268,294,348,370,376,408,415,426,438,443,471,476,482,490,503,518,549,560,564,575,588,608,627,654,718,722,764
#SBATCH --output=/scratch/users/briannac/logs/family_likelihoods_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_likelihoods_%a.err
#SBATCH --time=48:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total -- 727 should actually work.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods.sh

# SLURM_ARRAY_TASK_ID=1
cd $MY_HOME/alt_haplotypes
N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)

#if [  -f intermediate_files/family_likelihoods/unmapped/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then

    if [ ! -f intermediate_files/family_likelihoods/unmapped/global_regions_phasings_fam${N_digits}.tsv ]; then

        N_KMERS=$(wc -l data/kmers_unmapped_prev_and_median_filt.txt | awk '{print $1}') ### CHANGE DEPENDING ON FILE!
        ml python/3.6.1 
        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/unmapped/ \
             intermediate_files/family_likelihoods/kmers_unmapped_prev_and_median_filt_counts.tsv $N_KMERS
    fi
#fi


#if [  -f intermediate_files/family_likelihoods/ground_truth/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then

    #if [ ! -f intermediate_files/family_likelihoods/unplaced_decoy_sequences/global_regions_phasings_fam${N_digits}.tsv ]; then

      #  N_KMERS=$(wc -l data/unplaced_decoy_seqs_kmers.txt | awk '{print $1}') ### CHANGE DEPENDING ON FILE!
      #  ml python/3.6.1 
      #  python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/unplaced_decoy_seqs/ \
      #       data/unplaced_decoy_seqs_kmer_counts.tsv $N_KMERS
    #fi
#fi


### Fixing error..
#cd $MY_HOME/alt_haplotypes/intermediate_files/family_likelihoods/unmapped
#for lfile in likelihood_matrix_phasings_kmers_fam*.tsv; do
#    echo $lfile
#    mv $lfile $lfile.tmp
#    head -n 5679230 $lfile.tmp > $lfile
#    #\rm $lfile.tmp
#done




