#!/bin/bash
#SBATCH --job-name=shared_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/shared_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/shared_kmers.err
#SBATCH --time=10:00:00
#SBATCH --mem=120GB   
#SBATCH --cpus-per-task=16
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### Note: Took 03:48:03 hours and 24 GB of mem last time.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/shared_kmers.sh

module load biology
module load jellyfish

intermediate_dir=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/kmers

# Get list of kmers that were in at least 2 samples.
echo "jellyfish count..."
jellyfish count -t $SLURM_CPUS_PER_TASK -m 100 -L 2 -s 1000M -o $intermediate_dir/kmers.unmapped_reads.jf $intermediate_dir/*.jellyfish.unmapped_reads.fa

# Dump kmer count .jf to .fasta.
echo "jellyfish dump..."
jellyfish dump $intermediate_dir/kmers.unmapped_reads.jf  > $intermediate_dir/kmers.unmapped_reads.fasta

# Print all sequences to a list (take away >___ header)
echo "print to list..."
awk 'NR % 2 == 0' $intermediate_dir/kmers.unmapped_reads.fasta > $intermediate_dir/kmers.unmapped_reads.list

### Note: This resulted in 264,492,894 shared kmers.
