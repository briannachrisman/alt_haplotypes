#!/bin/sh
#SBATCH --job-name=localize_unmapped_last_couple
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/localize_unmapped_last_couple_%a.out
#SBATCH --error=/scratch/users/briannac/logs/localize_unmapped_last_couple_%a.err
#SBATCH --time=60:00:00
#SBATCH --mem=50G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 5679230 kmers (so 57 100,000-kmer regions) total.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/localize_unmapped_last_couple.sh

ml python/3.6.1 

#N=$((SLURM_ARRAY_TASK_ID))
#N_digits=$(printf "%03d" $N)






file=/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/family_likelihoods/unmapped/likelihood_matrix_phasings_kmers.tsv
newfile=$MY_SCRATCH/tmp/split_likelihood_matrix_phasings_kmers/split_likelihood_matrix_phasings_kmer
split -l 100000 -d -a 4 --additional-suffix=.tsv $file  $newfile # Split into many 1M line files.
echo "done splitting..."

cd $MY_HOME/alt_haplotypes


python3.6 -u src/localize/localize_unmapped_last_couple.py 47
echo "done with 47..."

python3.6 -u src/localize/localize_unmapped_last_couple.py 49
echo "done with 49..."
