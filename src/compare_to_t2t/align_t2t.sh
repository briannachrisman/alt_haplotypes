#!/bin/sh
#SBATCH --job-name=align_t2t
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/align_t2t.out
#SBATCH --error=/scratch/users/briannac/logs/align_t2t.err
#SBATCH --time=120:00:00
#SBATCH --mem=200G
#SBATCH --cpus-per-task=24
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
SAM=kmers_unmapped_filt_t2t_aligned.sam
BAM=kmers_unmapped_filt_t2t_aligned.bam

BED1=kmers_unmapped_filt_t2t_aligned_1v1.bed
BED_HG38=kmers_unmapped_filt_t2t_aligned_hg38.bed
BED_UNMAPPED=kmers_unmapped_filt_t2t_aligned_unmapped.bed
CHAIN=t2t-chm13-v1.1.grch38.over.chain.gz

# For testing
#TEST_FASTA=kmers_unmapped_filt_test.fasta
#head -n 1000 $FASTA > $TEST_FASTA

# Turn txt file of kmers to fasta file.
echo "Turning in fasta...."
head -n 104565782 $MY_HOME/alt_haplotypes/data/unmapped_kmers.txt  | awk '{ print ">"NR-1"\n"$0 }' > $FASTA

# Align.
echo "Aligning..."
bwa mem $REF $FASTA -o $SAM -t 24
echo "Done aligning"

# Convert to bam 
ml bedtools
bedtools bamtobed -i $BAM >  $BED1

# LIFT OVER TO NEW COORDINATES.
/oak/stanford/groups/dpwall/computeEnvironments/liftOver $BED1 $CHAIN $BED_HG38 $BED_UNMAPPED

# Liftover gaps in hg38 to T2T assembly.
cd $MY_HOME/alt_haplotypes/intermediate_files/t2t_comparison
awk -F'\t+' '{ print $1,($2-1),($3+1),$4}' OFS='\t'  /home/groups/dpwall/briannac/general_data/reference_genomes/hg38/hg38_agp_file.tsv > hg38_gaps_starts.bed

#cut -f 1,2,2,4 /home/groups/dpwall/briannac/general_data/reference_genomes/hg38/hg38_agp_file.tsv > hg38_gaps_starts.bed
#/oak/stanford/groups/dpwall/computeEnvironments/liftOver hg38_gaps_starts.bed grch38.t2t-chm13-v1.1.over.chain.gz \
#gaps_hg38_t2t_aligned_starts.bed  gaps_hg38_t2t_aligned_unmapped_starts.bed

