#!/bin/sh
#SBATCH --job-name=convert_localizations_t2t
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/convert_localizations_t2t.out
#SBATCH --error=/scratch/users/briannac/logs/convert_localizations_t2t.err
#SBATCH --time=20:00:00
#SBATCH --mem=70G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/convert_localizations_t2t.sh
ml python/3.6.1 

python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/convert_localizations_t2t.py

cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/
CHAIN=$MY_HOME/alt_haplotypes/intermediate_files/t2t_comparison/grch38.t2t-chm13-v1.1.over.chain.gz

/oak/stanford/groups/dpwall/computeEnvironments/liftOver -ends=100000 localized_regions_hg38_for_conversion.bed $CHAIN localized_regions_T2T.bed localized_regions_T2T_liftover_fail.bed

#python3.6 -u /home/groups/dpwall/briannac/alt_haplotypes/src/compare_to_t2t/clean_up_liftover_output.py
