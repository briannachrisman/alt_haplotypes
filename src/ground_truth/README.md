# Count Known Kmers
Computing matrix of sample x kmer corresponding to known/localized alternative haplotype in order to test accuracy / ground truth of algorithm.

## Storage

- **Intermediate files**: ```MY_HOME/alt_haplotypes/intermediate_results/ground_truth```
- **Final results**: ```MY_HOME/alt_haplotypes/results/ground_truth/kmer_count_matrix```

## Pipeline

1.  ✓ ```extract_known_kmers.ipynb```: Extract kmers from known localized alternative haplotypes. 
    - **Inputs**: ```MY_HOME/general_data/ref_genomes/hg38/hg38.fasta
    - **Outputs**: ```/home/groups/dpwall/briannac/alt_haplotypes/data/known_alt_haplotype_kmers.txt```

2.  ✓ ```count_known_kmers.sh```: Compute list of unique k-mers from localized alternative haplotypes. Note: 51,051,316 (510 batches) total kmers. 
    - ***Inputs***: ```s3://ihart-hg38/cram/<SAMPLE>.final.cram```
    - ***Outputs***: ```./intermediate_files/ground_truth/sample_kmer_counts/<SAMPLE>/kmer_counts.<KMER_BATCH>.txt```

4.  ✓ ```concat_kmer_counts.sh```: Concatenates sample kmer counts for each k-mer batch. 
    - ***Inputs***:  ```../intermediate_files/ground_truth/sample_kmer_counts/<SAMPLE>/kmer_counts.<KMER_BATCH>.txt``` 
    - ***Outputs***:  ```../intermediate_files/ground_truth/sample_kmer_matrix/kmers.<KMER_BATCH>.tsv.gz```
    
5.  ✓ ```filter_kmers.sh```: Filters kmers
    - ***Inputs***:  ```../intermediate_files/ground_truth/sample_kmer_counts/kmers.<KMER_BATCH>.tsv.gz``` 
    - ***Outputs***:  ```./intermediate_files/ground_truth/sample_kmer_matrix/known_alt_haplotype_kmers_filt.<KMER_BATCH>.txt```, ```./intermediate_files/ground_truth/sample_kmer_matrix/known_alt_haplotype_kmers_filt.<KMER_BATCH>.tsv```
    
6.  ✓ ```concat_filtered_kmers.sh```: Concatenates filtered kmers
    - ***Inputs***:  ```./intermediate_files/ground_truth/sample_kmer_matrix/known_alt_haplotype_kmers_filt.<KMER_BATCH>.txt```, ```./intermediate_files/ground_truth/sample_kmer_matrix/known_alt_haplotype_kmers_filt.<KMER_BATCH>.tsv```
    - ***Outputs***:  ```../data/known_kmers.txt```, ```../data/known_kmer_counts.tsv```