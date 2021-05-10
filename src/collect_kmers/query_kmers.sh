#!/bin/bash
#SBATCH --job-name=query_kmers
#SBATCH --partition=owners
#SBATCH --array=1-203
#SBATCH --output=/scratch/users/briannac/logs/query_kmers_%a.out
#SBATCH --error=/scratch/users/briannac/logs/query_kmers_%a.err
#SBATCH --time=20:00:00
#SBATCH --mem=10GB
####SBATCH --cpus-per-task=5
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

#python3.6 $MY_HOME/general_scripts/slurm_and_batch_resources/unfinished_samples.py $MY_HOME/alt_haplotypes/intermediate_files/kmers/ .query_counts.unmapped_reads.done $MY_HOME/general_data/samples_and_batches.tsv $MY_HOME/alt_haplotypes/intermediate_files/kmers/query_kmers_unfinished.tsv


### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/query_kmers.sh
ml biology
ml jellyfish

unfinished_samples=$MY_HOME/alt_haplotypes/intermediate_files/kmers/query_kmers_unfinished.tsv
intermediate_dir=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/kmers

## SLURM_ARRAY_TASK_ID=1
#SAMPLE=HI0203
cd $SCRATCH/tmp
for I_TO_ADD in 0
do
    N=$((SLURM_ARRAY_TASK_ID + I_TO_ADD))
    head -n $N $unfinished_samples | tail -n 1 > $SCRATCH/tmp/tmp_query_kmers_$SLURM_ARRAY_TASK_ID.txt
    while read SAMPLE _; do
        
        echo $SAMPLE
        # Put header (SAMPLE_ID) onto file.
        echo $SAMPLE > $intermediate_dir/$SAMPLE.query_counts.unmapped_reads.txt
            
        # For each 'shared' k-mer, query number of kmers in sample's .jf file.
        xargs jellyfish query $intermediate_dir/$SAMPLE.jellyfish.unmapped_reads.jf <$intermediate_dir/kmers.unmapped_reads.list \
        | awk  '{print $2}'  >> $intermediate_dir/$SAMPLE.query_counts.unmapped_reads.txt
        
        if [[ $(zgrep -Ec "$" $intermediate_dir/$SAMPLE.query_counts.unmapped_reads.txt) == 264492895 ]]; then
            echo "done" > $intermediate_dir/$SAMPLE.query_counts.unmapped_reads.done
        fi
    done < $SCRATCH/tmp/tmp_query_kmers_$SLURM_ARRAY_TASK_ID.txt
done
