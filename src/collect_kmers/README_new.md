# Count Unlocalized Kmers
Computing matrix of sample x kmer corresponding to known/localized alternative haplotype in order to test accuracy / ground truth of algorithm.

## Storage

- **Intermediate files**: ```MY_HOME/alt_haplotypes/intermediate_results/unplaced_decoy_seqs```
- **Final results**: ```MY_HOME/alt_haplotypes/results/unplaced_decoy_seqs/kmer_count_matrix```

## Pipeline

1.   ```extract_unknown_kmers.ipynb```: Extract kmers from unknown localized alternative haplotypes. 
    - **Inputs**: ```MY_HOME/general_data/ref_genomes/hg38/hg38.fasta
    - **Outputs**: ```/home/groups/dpwall/briannac/alt_haplotypes/data/unknown_alt_haplotype_kmers.txt```

2.  ```count_unknown_kmers.sh```: Compute list of unique k-mers from localized alternative haplotypes. Note: 51,051,316 total kmers. 
    - ***Inputs***: ```s3://ihart-hg38/cram/<SAMPLE>.final.cram```
    - ***Outputs***: ```./intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.txt```

3.  ```concat_kmer_counts.sh```: Concatenates sample kmer counts for each region.
    - ***Inputs***:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.<REGION>.txt``` 
    - ***Inputs***:  ```../results/unplaced_decoy_seqs/kmer_count_matrix/kmer_counts.<REGION>.tsv.gz```
    
4.  ```filter_kmers.sh```: Concatenates sample kmer counts for each region.
    - ***Inputs***:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.<REGION>.txt``` 
    - ***Inputs***:  ```../results/unplaced_decoy_seqs/kmer_count_matrix/kmer_counts.<REGION>.tsv.gz```
    
5.  ```concat_filtered_kmers.sh```: Concatenates sample kmer counts for each region.
    - ***Inputs***:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.<REGION>.txt``` 
    - ***Inputs***:  ```../results/unplaced_decoy_seqs/kmer_count_matrix/kmer_counts.<REGION>.tsv.gz```