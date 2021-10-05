#!/bin/sh
#SBATCH --job-name=cluster
#SBATCH --partition=dpwall
#SBATCH --array=16
#SBATCH --output=/scratch/users/briannac/logs/cluster_%a.out
#SBATCH --error=/scratch/users/briannac/logs/cluster_%a.err
#SBATCH --time=10:00:00
#SBATCH --mem=100GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at $MY_HOME/alt_haplotypes/src/de_novo_assemble/cluster.sh
### Note: Job took about ____ time, ___ mem consumption, 23 batches to run.

ml python/3.6.1

# Clean and set up directories.
\rm /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/de_novo_assemble/chr${SLURM_ARRAY_TASK_ID} -r
mkdir /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/de_novo_assemble/chr${SLURM_ARRAY_TASK_ID}


# Run clustering script.
python3.6 -u $MY_HOME/alt_haplotypes/src/de_novo_assemble/cluster.py $SLURM_ARRAY_TASK_ID

# Run de novo assembly.
for file in /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/de_novo_assemble/chr${SLURM_ARRAY_TASK_ID}/*.fasta ; do
    echo "ASSEMBLING" ${file}
    assembled_dir="${file/.fasta/_assembled}"

    # Remove previous directory to start clean.
    \rm ${assembled_dir} -r
    
    # Assemble.
    megahit -r $file -o ${assembled_dir}
done

