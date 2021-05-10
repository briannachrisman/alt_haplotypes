#!/bin/bash
#SBATCH --job-name=kmers_from_unmapped_reads
#SBATCH --partition=dpwall
#SBATCH --array=2
#SBATCH --output=/scratch/users/briannac/logs/kmers_from_unmapped_reads_%a.out
#SBATCH --error=/scratch/users/briannac/logs/kmers_from_unmapped_reads_%a.err
#SBATCH --time=04:00:00
#SBATCH --mem=120GB
####SBATCH --cpus-per-task=5
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/kmers_from_unmapped_reads.sh
SLURM_ARRAY_TASK_ID=2 ### CHANGE FOR BATCH ###

###########
# Note: Before kicking off batch, run 

#find $MY_HOME/alt_haplotypes/intermediate_files/kmers/*jellyfish*fa -size 0 -print -delete

#python3.6 $MY_HOME/general_scripts/slurm_and_batch_resources/unfinished_samples.py $MY_HOME/alt_haplotypes/intermediate_files/kmers/ .jellyfish.unmapped_reads.fa $MY_HOME/general_data/samples_and_batches.tsv $MY_HOME/alt_haplotypes/intermediate_files/kmers/kmers_from_unmapped_reads_unfinished.tsv

###########

ml biology
ml jellyfish
unfinished_samples=$MY_HOME/alt_haplotypes/intermediate_files/kmers/kmers_from_unmapped_reads_unfinished.tsv

# Directories of extracted fastq files.
fastq_dir=/home/groups/dpwall/briannac/blood_microbiome/intermediate_files/kraken_align
intermediate_dir=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/kmers

cd $SCRATCH/tmp
for I_TO_ADD in 0 #1000 2000 3000
do
    N=$((SLURM_ARRAY_TASK_ID + I_TO_ADD))
    head -n $N $unfinished_samples | tail -n 1 > $SCRATCH/tmp/tmp_kmers_from_unmapped_reads_$SLURM_ARRAY_TASK_ID.txt
    while read SAMPLE BATCH; do
        echo $SAMPLE $BATCH
        
        # Kmers in unmapped reads.
        # Count kmers (depth >=2)
        depth=2
        echo "Counting kmers..."
        jellyfish count --canonical -m 100 -s 100M -L $depth ${fastq_dir}/${SAMPLE}.unclassified.fastq  \
        -o $MY_HOME/alt_haplotypes/intermediate_files/kmers/$SAMPLE.jellyfish.unmapped_reads.jf
            
         # Dump to fasta file.
         echo "dumping to fasta..."
         jellyfish dump $intermediate_dir/$SAMPLE.jellyfish.unmapped_reads.jf > $intermed
        
        
    done < $SCRATCH/tmp/tmp_kmers_from_unmapped_reads_$SLURM_ARRAY_TASK_ID.txt
    \rm $SCRATCH/tmp/tmp_kmers_from_unmapped_reads_$SLURM_ARRAY_TASK_ID.txt 
done
