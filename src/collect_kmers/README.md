# Collect k-mers
Extracting common(ish) kmers & counts from ultimately unmapped reads.

## Storage
- **Intermediate files**: ```HOME/alt_haplotypes/intermediate_results/kmers```
- **Final results**: ```HOME/alt_haplotypes/results/kmers```

## Prerequisites

0.1. Kraken_align pipeline. Relaign reads from iHART that did not align/aligned poorly to hg38 to a database of archaea, human, bacteria, and viral sequences.

## Pipeline

1.  ✓ ```kmers_from_unmapped_reads.sh```: Extract kmers from ultimately unmapped reads. (PS: can use get_unfinished_samples.ipynb to update finished/unfinished samples)
    - ***Inputs***: ``../blood_microbiome/intermediate_files/kraken_align/<SAMPLE>.unclassified.fastq```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.unmapped.jf```, ```../intermediate_files/kmers/<SAMPLE>.jellyfish.unmapped.fa```

2. ✓ ```shared_kmers.sh```: Compute list of non-unique k-mers. Note: 264,492,894 total shared kmers.
    - ***Inputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.kmers.unmapped_reads.list.fa```
    - ***Outputs***: ```../intermediate_files/kmers/kmers.kmers.unmapped_reads.list.list```

3. ✓ ```query_kmers.sh```: Query each sample for count of each non-unique kmers (Can use get_unfinished_samples.ipynb to update finished/unfinished samples) ***TODO: Currently running.***
    - ***Inputs***: ```../intermediate_files/kmers/kmers.kmers.unmapped_reads.list```, ```../intermediate_files/kmers/<SAMPLE>.jellyfish.kmers.unmapped_reads.list.jf```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.query_counts.kmers.unmapped_reads.list.txt```

4. ✓ ```split_kmer_counts.sh```: Splits each sample kmer counts into many different files/kmer sets for concatenation.
    - ***Inputs***:  ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.query_counts.unmapped_reads.txt```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.query_counts.unmapped_reads.<KMER_REGION>.txt```    
     ***Currently Running: 3,971 finished as of 5/14/2021. ***

6. ```concat_kmer_counts.sh```: Concatenates sample kmer counts for each region.
    - ***Inputs***:  ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.query_counts.unmapped_reads.list.txt```
    - ***Outputs***: ```../intermediate_files/kmers/query_counts.unmapped_reads.<KMER_REGION>.tsv```
    
7. ```move_to_results.sh```: Move to permanent results directory.
    - ***Inputs***: ```../intermediate_files/kmers/query_counts.unmapped_reads.<KMER_REGION>.tsv```
    - ***Outputs***: ```../results/kmers/query_counts.unmapped_reads.<KMER_REGION>.tsv.gz```


Note: Ran ```move.sh``` and ```organize_directories.sh``` to reorganize file structure a bit to make linux commands run faster.