#!/bin/sh
#SBATCH --job-name=concat_kmer_counts
#SBATCH --partition=owners
#SBATCH --array=5-511
#SBATCH --output=/scratch/users/briannac/logs/concat_kmer_counts_%a.out
#SBATCH --error=/scratch/users/briannac/logs/concat_kmer_counts_%a.err
#SBATCH --time=1:00:00
#SBATCH --mem=5G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 511 regions total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/ground_truth/concat_kmer_counts.sh
N=$((SLURM_ARRAY_TASK_ID-1))
N=$(printf "%03g" $N)

cd $MY_HOME/alt_haplotypes/intermediate_files/ground_truth

if [ ! -f $MY_HOME/alt_haplotypes/results/ground_truth/sample_kmer_matrix/kmers.$N.tsv.gz ]; then

    # Transform sample/batch matrix into list of file names.
    cut -f1 $MY_HOME/general_data/samples_and_batches.tsv  > $MY_SCRATCH/tmp/concat_known_kmers.$N.out
    sed -i -e "s/$/\/kmer_counts.$N.txt/" $MY_SCRATCH/tmp/concat_known_kmers.$N.out
    sed -i -e 's/^/sample_kmer_counts\//' $MY_SCRATCH/tmp/concat_known_kmers.$N.out
    

    # Paste files in same order as header
    echo "Pasting files together..."
    mapfile -t <$MY_SCRATCH/tmp/concat_known_kmers.$N.out
    paste "${MAPFILE[@]}" > $MY_SCRATCH/tmp/concat_known_kmers.$N.tsv
    
    # Add header.
    echo "Adding header..."
    cat /home/groups/dpwall/briannac/general_data/samples_header.tsv $MY_SCRATCH/tmp/concat_known_kmers.$N.tsv > $MY_SCRATCH/tmp/concat_known_kmers.$N.final.tsv

    
    # Zip and remove intermediate files to save some space.
    echo "zipping..."
    gzip  $MY_SCRATCH/tmp/concat_known_kmers.$N.final.tsv -f
    
    echo "moving to OAK..."
    mv $MY_SCRATCH/tmp/concat_known_kmers.$N.final.tsv.gz $MY_HOME/alt_haplotypes/results/ground_truth/sample_kmer_matrix/kmers.$N.tsv.gz
    # $MY_HOME/alt_haplotypes/results/ground_truth/sample_kmer_matrix/kmers.$N.tsv -f
    
    echo "Cleaning up..."
    \rm $MY_SCRATCH/tmp/concat_known_kmers.$N.tsv
    \rm $MY_SCRATCH/tmp/concat_known_kmers.$N.out

fi


