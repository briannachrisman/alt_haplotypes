#!/bin/sh
#SBATCH --job-name=organize_directories_collect_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/organize_directories_collect_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/organize_directories_collect_kmers.err
#SBATCH --time=40:00:00
#SBATCH --mem=1G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/organize_directories.sh

cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/kmers
while read SAMPLE _; do
    echo "running" $SAMPLE
    mkdir $SAMPLE
    mv $SAMPLE.query_counts.unmapped_reads.txt.gz $SAMPLE/$SAMPLE.query_counts.unmapped_reads.txt.gz
    mv $SAMPLE.query_counts.unmapped_reads.txt $SAMPLE/$SAMPLE.query_counts.unmapped_reads.txt
    mv $SAMPLE.jellyfish.unmapped_reads.jf $SAMPLE/$SAMPLE.jellyfish.unmapped_reads.jf
    mv $SAMPLE.jellyfish.unmapped_reads.fa $SAMPLE/$SAMPLE.jellyfish.unmapped_reads.fa
    mv $SAMPLE.query_counts.unmapped_reads.done $SAMPLE/$SAMPLE.query_counts.unmapped_reads.done
    for i in {0..2644}; do
        N=$(printf "%04g" $i)
        mv $SAMPLE.query_counts.unmapped_reads.$N.txt $SAMPLE/$SAMPLE.query_counts.unmapped_reads.$N.txt
    done
done < $MY_HOME/general_data/samples_and_batches.tsv