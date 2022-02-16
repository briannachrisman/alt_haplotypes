#!/bin/sh
#SBATCH --job-name=construct_synthetic_dataset
#SBATCH --partition=owners
#SBATCH --output=/scratch/users/briannac/logs/construct_synthetic_dataset.out
#SBATCH --error=/scratch/users/briannac/logs/construct_synthetic_dataset.err
#SBATCH --time=20:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/construct_datasets/construct_synthetic_datasets.sh

ml python/3.6

for REPEATS in 1 10 100; do
    python3.6 -u $MY_HOME/alt_haplotypes/src/construct_datasets/construct_synthetic_datasets.py $REPEATS 100000
    python3.6 -u $MY_HOME/alt_haplotypes/src/construct_datasets/construct_synthetic_datasets_y_chrom.py $REPEATS 1000
    cat $MY_HOME/alt_haplotypes/data/counts/synthetic_data_y_chrom_${REPEATS}_repeats.tsv $MY_HOME/alt_haplotypes/data/counts/synthetic_data_${REPEATS}_repeats.tsv > $MY_HOME/alt_haplotypes/data/counts/synthetic_data_${REPEATS}_repeats_all.tsv 
done

cat $MY_HOME/alt_haplotypes/data/counts/synthetic_data_locations_y.txt $MY_HOME/alt_haplotypes/data/counts/synthetic_data_locations.txt  > $MY_HOME/alt_haplotypes/data/counts/synthetic_data_locations_all.txt 


cp $MY_HOME/alt_haplotypes/data/counts/*all.tsv $MY_HOME/alt_haplotypes/intermediate_files/counts