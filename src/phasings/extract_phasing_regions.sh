#!/bin/bash

phasings_dir=/home/groups/dpwall/briannac/alt_haplotypes/data/phasings
cd $phasings_dir
# Extract chromsome, start pos, and end pos from Kelley's phasing files.

awk 'NR>1 {print $2}' phased_fams/*.txt > \
$phasings_dir/chrom.txt

awk 'NR>1 {print $(NF-1)}' phased_fams/*.txt > \
$phasings_dir/start.txt

awk 'NR>1 {print $NF}' phased_fams/*.txt > \
$phasings_dir/end.txt

paste $phasings_dir/chrom.txt $phasings_dir/start.txt $phasings_dir/end.txt | sort | uniq > $phasings_dir/regions.tsv

sed -i '/start_pos/d' $phasings_dir/regions.tsv # Delete the accidental header line that got mixed in during sort.

python3.6 $MY_HOME/alt_hapltotypes/phasings/sort_regions.py

\rm $phasings_dir/regions.tsv 
\rm $phasings_dir/start.txt
\rm $phasings_dir/end.txt
\rm $phasings_dir/chrom.txt


mv $phasings_dir/regions_sorted.tsv  $phasings_dir/regions.tsv