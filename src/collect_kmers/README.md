# Collect k-mers

## Storage
- **Intermediate files**: ```HOME/alt_haplotypes/intermediate_results/kmers```
- **Final results**: ```HOME/alt_haplotypes/results/kmers```

## Prerequisites

0.1. Kraken_align pipeline. Relaign reads from iHART that did not align/aligned poorly to hg38 to a database of archaea, human, bacteria, and viral sequences.

## Pipeline

1.  ✓ ```kmers_from_unmapped_reads.sh```: Extract kmers from ultimately unmapped reads. (PS: can use get_unfinished_samples.ipynb to update finished/unfinished samples)
    - ***Inputs***: ``../blood_microbiome/intermediate_files/kraken_align/<SAMPLE>.unclassified.fastq```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>.jellyfish.unmapped.jf```, ```../intermediate_files/kmers/<SAMPLE>.jellyfish.unmapped.fa```

2. ✓ ```shared_kmers.sh```: Compute list of non-unique k-mers. Note: 264,492,894 total shared kmers.
    - ***Inputs***: ```../intermediate_files/kmers/<SAMPLE>.jellyfish.kmers.unmapped_reads.list.fa```
    - ***Outputs***: ```../intermediate_files/kmers/kmers.kmers.unmapped_reads.list.list```

3. ✓ ```query_kmers.sh```: Query each sample for count of each non-unique kmers (Can use get_unfinished_samples.ipynb to update finished/unfinished samples) ***TODO: Currently running.***
    - ***Inputs***: ```../intermediate_files/kmers/kmers.kmers.unmapped_reads.list.list```, ```../intermediate_files/kmers/<SAMPLE>.jellyfish.kmers.unmapped_reads.list.jf```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>.query_counts.kmers.unmapped_reads.list.txt```

4. ```split_kmer_counts.sh```: Compute count matrix of kmer x sample.   ***TODO: Currently Running***
    - ***Inputs***:  ```../intermediate_files/kmers/<SAMPLE>.query_counts.kmers.unmapped_reads.list.txt```
    - ***Outputs***: ```../results/kmers/kmer_counts.kmers.unmapped_reads.list.tsv```    

5. ```concat_kmer_counts.sh```: Compute count matrix of kmer x sample.   
    - ***Inputs***:  ```../intermediate_files/kmers/<SAMPLE>.query_counts.kmers.unmapped_reads.list.txt```
    - ***Outputs***: ```../results/kmers/kmer_counts.kmers.unmapped_reads.list.tsv```
