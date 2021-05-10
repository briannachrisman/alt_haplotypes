#!/bin/bash
#SBATCH --job-name=remove_unfinished_query_kmers
#SBATCH --partition=dpwall
#SBATCH --output=/scratch/users/briannac/logs/remove_unfinished_query_kmers.out
#SBATCH --error=/scratch/users/briannac/logs/remove_unfinished_query_kmers.err
#SBATCH --time=30:00:00
#SBATCH --mem=128GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu


### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/remove_unfinished_query_kmers.sh

ml parallel

check_length() {
    if [[ $(zgrep -Ec "$" $1) == 264492895 ]]; then
        #echo "do1ne "> ${file/.unmapped.txt/.done}
        echo $1 finished
    else
        \rm ${1/txt/done}
        \rm $file
        echo $1 not finished
    fi
}

export -f check_length
parallel -j 20 check_length ::: $MY_HOME/alt_haplotypes/intermediate_files/kmers/*.query_counts.unmapped_reads.txt