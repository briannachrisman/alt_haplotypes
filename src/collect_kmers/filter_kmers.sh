#!/bin/sh
#SBATCH --job-name=filter_kmers
#SBATCH --partition=owners
#SBATCH --array=2-1000
#SBATCH --output=/scratch/users/briannac/logs/filter_kmers_%a.out
#SBATCH --error=/scratch/users/briannac/logs/filter_kmers_%a.err
#SBATCH --time=1:00:00
#SBATCH --mem=100G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/collect_kmers/filter_kmers.sh
# array should be 2644

# SLURM_ARRAY_TASK_ID=1
ml python/3.6
for i in 0 1000 2000; do
    echo $i
    N=$((SLURM_ARRAY_TASK_ID-1+i))
    echo $N
    Nzeros=$(printf %04d $N)
    if [ ! -f /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/unmapped/filt/kmers_unmapped.${Nzeros}.txt ]; then
        echo running
        python3.6 -u $MY_HOME/alt_haplotypes/src/collect_kmers/filter_kmers.py $N
    fi
done