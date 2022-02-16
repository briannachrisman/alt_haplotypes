#!/bin/sh
#SBATCH --job-name=align_t2t
#SBATCH --partition=owners
#SBATCH --output=/scratch/users/briannac/logs/align_t2t.out
#SBATCH --error=/scratch/users/briannac/logs/align_t2t.err
#SBATCH --time=40:00:00
#SBATCH --mem=100G
#SBATCH --cpus-per-task=100
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/align_t2t.sh

# Index reference genome.
echo "Indexing..."
cd /home/groups/dpwall/briannac/general_data/reference_genomes/t2t
#bwa index chm13.draft_v1.1.fasta

# Set up files.
cd $MY_HOME/alt_haplotypes/intermediate_files/t2t_comparison
REF=/home/groups/dpwall/briannac/general_data/reference_genomes/t2t/chm13.draft_v1.1.fasta
FASTA=kmers_unmapped_filt.fasta
BAM=kmers_unmapped_filt_t2t_aligned.bam

# For testing
TEST_FASTA=kmers_unmapped_filt_test.fasta
head -n 1000 $FASTA > $TEST_FASTA

# Turn txt file of kmers to fasta file.
#echo "Turning in fasta...."
#awk '{ print ">"NR-1"\n"$0 }' $MY_HOME/alt_haplotypes/data/kmers_unmapped_filt.txt > $FASTA

# Align.
echo "Aligning..."
bwa mem $REF $FASTA -o $BAM -t 100
echo "Done aligning"



