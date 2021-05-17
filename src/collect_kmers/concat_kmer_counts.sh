#!/bin/sh
#SBATCH --job-name=concat_kmer_counts
#SBATCH --partition=owners
#SBATCH --array=2-1000
#SBATCH --output=/scratch/users/briannac/logs/concat_kmer_counts_%a.out
#SBATCH --error=/scratch/users/briannac/logs/concat_kmer_counts_%a.err
#SBATCH --time=1:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu


### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/concat_kmer_counts.sh

for i in 0 1000 2000; do
    N=$((SLURM_ARRAY_TASK_ID-1+i))
    N=$(printf "%04g" $N)
    if [ ! -f $MY_HOME/alt_haplotypes/results/kmers/query_counts.unmapped_reads/query_counts.unmapped_reads.$N.tsv.gz ]; then
        mkdir $MY_SCRATCH/tmp/alt_haplotypes/$N
        while read SAMPLE BATCH; do
            file=$MY_HOME/alt_haplotypes/intermediate_files/kmers/$SAMPLE/$SAMPLE.query_counts.unmapped_reads.$N.txt;
            sed  '/[*]/d' $file > $MY_SCRATCH/tmp/alt_haplotypes/$N/$SAMPLE.query_counts.unmapped_reads.$N.txt
            echo 'cleaned up' $file
        done < $MY_HOME/general_data/samples_and_batches.tsv
        echo "pasting..."
        paste $MY_SCRATCH/tmp/alt_haplotypes/$N/*.query_counts.unmapped_reads.$N.txt > $MY_SCRATCH/tmp/alt_haplotypes/$N/query_counts.unmapped_reads.$N.tsv
        gzip -f $MY_SCRATCH/tmp/alt_haplotypes/$N/query_counts.unmapped_reads.$N.tsv 
        mv $MY_SCRATCH/tmp/alt_haplotypes/$N/query_counts.unmapped_reads.$N.tsv.gz $MY_HOME/alt_haplotypes/results/kmers/query_counts.unmapped_reads/query_counts.unmapped_reads.$N.tsv.gz
        \rm $MY_SCRATCH/tmp/alt_haplotypes/$N -r
    fi

done
