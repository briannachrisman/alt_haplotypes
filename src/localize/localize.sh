#!/bin/sh
#SBATCH --job-name=localize_unmapped
#SBATCH --partition=owners
#SBATCH --array=381,709,807,812,850,868,878,885,931,998
#SBATCH --output=/scratch/users/briannac/logs/localize_unmapped_%a.out
#SBATCH --error=/scratch/users/briannac/logs/localize_unmapped_%a.err
#SBATCH --time=20:00:00
#SBATCH --mem=70G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize.sh

# Note: Change to fit however many sequences we are trying to localize / 100000

ml python/3.6.1 

N=$((SLURM_ARRAY_TASK_ID))
N_digits=$(printf "%04d" $N)
N_digits_minus_one=$((N-1))
N_digits_minus_one=$(printf "%04d" ${N_digits_minus_one})


if [ ! -f /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits_minus_one}.tsv ]; then 
    cd $MY_HOME/alt_haplotypes

    python3.6 -u src/localize/localize_unmapped.py $N  intermediate_files/family_likelihoods/unmapped/ intermediate_files/localize/unmapped/ 100000
fi



echo "converting to bed..."
N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%04d" $N)
if [ ! -f /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_end_with_Y.bed ]; then 

    python3.6 -u src/compare_to_t2t/convert_unmapped_localizations.py $N
    CHAIN=$MY_HOME/alt_haplotypes/intermediate_files/t2t_comparison/grch38.t2t-chm13-v1.1.over.chain.gz

    echo "coverting starts..."
    BED_IN=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_start.bed
    BED_OUT=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_T2T_start.bed
    BED_UNMAPPED=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_start_unmapped.bed

    /oak/stanford/groups/dpwall/computeEnvironments/liftOver $BED_IN $CHAIN $BED_OUT $BED_UNMAPPED

    echo "converting ends..."
    BED_IN=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_end.bed
    BED_OUT=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_T2T_end.bed
    BED_UNMAPPED=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_${N_digits}_end_unmapped.bed

    /oak/stanford/groups/dpwall/computeEnvironments/liftOver $BED_IN $CHAIN $BED_OUT $BED_UNMAPPED
fi


# Convert localized to BED

#python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/synthetic_data10/ intermediate_files/localize/synthetic_data10/ 101000


#python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/synthetic_data100/ intermediate_files/localize/synthetic_data100/ 101000



#python3.6 -u src/localize/localize.py $N  intermediate_files/family_likelihoods/decoy_known/ intermediate_files/localize/unmapped/ 10000
# This should be array 1-110
