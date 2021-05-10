#!/bin/bash
#SBATCH --job-name=clean_phasing
#SBATCH --partition=dpwall
#SBATCH --array=1-61%10
#SBATCH --output=/scratch/users/briannac/logs/clean_phasing_%a.out
#SBATCH --error=/scratch/users/briannac/logs/clean_phasing_%a.err
#SBATCH --time=10:00
#SBATCH --mem=2GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/clean_phasing.sh

## SLURM_ARRAY_TASK_ID=1 ### CHANGE WHEN RUNNING BATCH!!!

#python3.6 $MY_HOME/general_scripts/slurm_and_batch_resources/unfinished_samples.py $MY_HOME/alt_haplotypes/data/phasings/phased_fams/ .txt $MY_HOME/alt_haplotypes/intermediate_files/phasings/fams_to_phase.csv  $MY_HOME/alt_haplotypes/intermediate_files/phasings/fams_unfinished.tsv 

unfinished_fams=$MY_HOME/alt_haplotypes/intermediate_files/phasings/fams_unfinished.tsv

cd $SCRATCH/tmp
head -n $SLURM_ARRAY_TASK_ID $unfinished_fams | tail -n 1 > $SCRATCH/tmp/tmp_phasings_$SLURM_ARRAY_TASK_ID.txt
while read FAM; do
    echo $FAM
    python3.6 /home/groups/dpwall/briannac/alt_haplotypes/src/phasings/clean_phasing.py $FAM
done < $SCRATCH/tmp/tmp_phasings_$SLURM_ARRAY_TASK_ID.txt
\rm $SCRATCH/tmp/tmp_phasings_$SLURM_ARRAY_TASK_ID.txt

