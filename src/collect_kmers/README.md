# Count Unlocalized Kmers

Computing matrix of sample x kmer corresponding to known/localized alternative haplotype in order to test accuracy / ground truth of algorithm.

## Pre-requisites
Run kraken pipeline to align unmapped reads to bacterial/viral sequences.

## Storage
Final results of kmer x sample matrix should be in ```../data/kmers_unmapped_counts_filt.tsv``` and ```../data/kmers_unmapped.txt```.

## Pipeline

1.  ✓ ```kmers_from_unmapped_reads.sh```: Extract kmers from ultimately unmapped reads. (PS: can use get_unfinished_samples.ipynb to update finished/unfinished samples)
    - ***Inputs***: ``../blood_microbiome/intermediate_files/kraken_align/<SAMPLE>.unclassified.fastq```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.unmapped.jf```, ```../intermediate_files/kmers/<SAMPLE>.jellyfish.unmapped.fa```

2. ✓ ```shared_kmers.sh```: Compute list of non-unique k-mers. Note: 264,492,894 total shared kmers.
    - ***Inputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.kmers.unmapped_reads.fa```
    - ***Outputs***: ```../intermediate_files/kmers/kmers.unmapped_reads.list```

3. ✓ ```query_kmers.sh```: Query each sample for count of each non-unique kmers (Can use get_unfinished_samples.ipynb to update finished/unfinished samples). Note 157,450,110 total non-unique k-mers.
    - ***Inputs***: ```../intermediate_files/kmers/kmers_all.list```, 
    ```../intermediate_files/kmers/<SAMPLE>.jellyfish.kmers.unmapped_reads.list.jf```
    - ***Outputs***: ```../intermediate_files/unmapped/query_counts.unmapped_reads.<SPLIT>.tsv.gz```

4. ✓ ```split_kmer_counts.sh```: Splits each sample kmer counts into many different files/kmer sets for concatenation.
    - ***Inputs***:  ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.query_counts.unmapped_reads.txt```
    - ***Outputs***: ```../intermediate_files/unmapped/query_counts.unmapped_reads.<KMER_BATCH>.txt```    

4.  ```filter_kmers.sh```: Filters kmers & counts based on prevalence and median. Total # of filtered kmers was 5,679,230.
    - ***Inputs***:  ```../intermediate_files/unmapped/query_counts.unmapped_reads.<KMER_BATCH>.txt```    
    - ***Outputs***:  ```../intermediate_files/unmapped/filt/kmers_unmapped_counts.<KMER_BATCH>.tsv```,
    ```../intermediate_files/unmapped/filt/kmers_unmapped.<KMER_BATCH>.txt``` 
    
5.  ```concat_filtered_kmers.sh```: Concatenates sample kmer counts for each region.
    - ***Inputs***:  ```../intermediate_files/unmapped/filt/kmers_unmapped_counts.<KMER_BATCH>.tsv```,
    ```../intermediate_files/unmapped/filt/kmers_unmapped.<KMER_BATCH>.txt``` 
    - ***Inputs***:  ```../data/kmers_unmapped_counts_prev_and_median_filt_counts.tsv```, ```../data/kmers_unmapped_counts_prev_and_median_filt.txt```
    

Note: Ran ```move.sh``` and ```organize_directories.sh``` to reorganize file structure a bit to make linux commands run faster.