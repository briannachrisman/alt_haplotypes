#!/bin/sh
#SBATCH --job-name=split_kmer_counts
#SBATCH --partition=dpwall
#SBATCH --array=11
#SBATCH --output=/scratch/users/briannac/logs/split_kmer_counts_%a.out
#SBATCH --error=/scratch/users/briannac/logs/split_kmer_counts_%a.err
#SBATCH --time=40:00:00
#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/collect_kmers/split_kmer_counts.sh

cd /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/kmers

ml parallel 
split_func() {
    
    echo $1
    sample=$1
    txtfile=${sample}/${sample}.query_counts.unmapped_reads.txt
    if [ -f $txtfile ]; then
        echo "deleting first line"
        if [ $(sed -n "1{/^$sample/p};q" $txtfile) ]; then
            tail -n +2 "$txtfile" > "$txtfile.tmp" && mv "$txtfile.tmp" "$txtfile" # Remove first line of file (sample name), shouldn't have added this in the first place.
        fi

        echo "splitting file"
        split -l 100000 -d -a 4 --additional-suffix=.txt $txtfile ${txtfile/.txt/.} # Split into many 1M line files.

        # Add sample name to start of all files.
        echo "Adding sample name to split files"
        for f in ${sample}/${sample}.query_counts.unmapped_reads.*.txt; do 
            sed  -i "1i $sample" $f
        done

        echo "zipping back up to save space"
        gzip $txtfile # Zip back up to save some space.
    fi
}

export -f split_func

N=$((SLURM_ARRAY_TASK_ID -1))
N=$(printf "%01g" $N)

for f in *$N; do
    split_func $f
done

#for f in *LCL; do
#    split_func $f
#done


#for f in *prep; do
#    split_func $f
#done


#parallel -j $SLURM_CPUS_PER_TASK split_func ::: *$N.query_counts.unmapped_reads.txt

# after all arrays done, do (for _LCL, _reprep samples): parallel -j 20 split_func ::: *LCL and *reprep
# do ls /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/kmers/*/*.query_counts.unmapped_reads.txt.gz | wc -l to see how many have completed
