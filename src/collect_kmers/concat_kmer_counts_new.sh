#!/bin/sh
#SBATCH --job-name=concat_kmer_counts
#SBATCH --partition=owners
#SBATCH --array=1-138
#SBATCH --output=/scratch/users/briannac/logs/concat_kmer_counts_%a.out
#SBATCH --error=/scratch/users/briannac/logs/concat_kmer_counts_%a.err
#SBATCH --time=1:00:00
#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 137 regions total.
### file at /home/groups/dpwall/briannac/alt_haplotypes/src/unplaced_decoy_seqs/concat_kmer_counts.sh
N=$((SLURM_ARRAY_TASK_ID-1))
N=$(printf "%03g" $N)

cd $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs

if [ ! -f $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/kmers.$N.tsv.gz ]; then

    # Transform sample/batch matrix into list of file names.
    cut -f1 $MY_HOME/general_data/samples_and_batches.tsv  > $MY_SCRATCH/tmp/concat_unknown_kmers.$N.out
    sed -i -e "s/$/\/kmer_counts.$N.txt/" $MY_SCRATCH/tmp/concat_unknown_kmers.$N.out
    sed -i -e 's/^/sample_kmer_counts\//' $MY_SCRATCH/tmp/concat_unknown_kmers.$N.out
    

    # Paste files in same order as header
    echo "Pasting files together..."
    mapfile -t <$MY_SCRATCH/tmp/concat_unknown_kmers.$N.out
    paste "${MAPFILE[@]}" > $MY_SCRATCH/tmp/concat_unknown_kmers.$N.tsv
    
    # Add header.
    echo "Adding header..."
    cat /home/groups/dpwall/briannac/general_data/samples_header.tsv $MY_SCRATCH/tmp/concat_unknown_kmers.$N.tsv > $MY_SCRATCH/tmp/concat_unknown_kmers.$N.final.tsv

    
    # Zip and remove intermediate files to save some space.
    echo "zipping..."
    gzip  $MY_SCRATCH/tmp/concat_unknown_kmers.$N.final.tsv -f
    
    echo "moving to OAK..."
    mv $MY_SCRATCH/tmp/concat_unknown_kmers.$N.final.tsv.gz $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/kmers.$N.tsv.gz
    # $MY_HOME/alt_haplotypes/results/unplaced_decoy_seqs/sample_kmer_matrix/kmers.$N.tsv -f
    
    echo "Cleaning up..."
    \rm $MY_SCRATCH/tmp/concat_unknown_kmers.$N.tsv
    \rm $MY_SCRATCH/tmp/concat_unknown_kmers.$N.out

fi


#for i in {0..137}; do 
#    N=$((i-1))
#    N=$(printf "%03g" $N)
#    if [ ! -f $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/kmers.$N.tsv.gz ]; then
#    echo $i
#    fi
#done