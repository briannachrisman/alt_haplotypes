# Count Unlocalized Kmers
Computing matrix of sample x kmer corresponding to known/localized alternative haplotype in order to test accuracy / ground truth of algorithm.

## Storage

- **Intermediate files**: ```MY_HOME/alt_haplotypes/intermediate_results/unplaced_decoy_seqs```
- **Final results**: ```MY_HOME/alt_haplotypes/results/unplaced_decoy_seqs/kmer_count_matrix```

## Pipeline

1.   ```extract_unknown_kmers.ipynb```: Extract kmers from unknown localized alternative haplotypes. 
    - **Inputs**: ```MY_HOME/general_data/ref_genomes/hg38/hg38.fasta
    - **Outputs**: ```/home/groups/dpwall/briannac/alt_haplotypes/data/unknown_alt_haplotype_kmers.txt```--> ```intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/unknown_alt_haplotype_kmers.txt```

2.  ```count_unknown_kmers.sh```: Compute list of unique k-mers from localized alternative haplotypes. Note: 13,665,769 total kmers. 
    - **Inputs***: ```s3://ihart-hg38/cram/<SAMPLE>.final.cram```,```intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/unknown_alt_haplotype_kmers.txt```
    - **Outputs**: ```./intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.<KMER_BATCH>txt```

3.  ```concat_kmer_counts.sh```: Concatenates sample kmer counts for each kmer batch.
    - **Inputs**:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.<KMER_BATCH>.txt``` 
    - **Outputs**:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/kmers.<KMER_BATCH>.tsv.gz```
    
4.  ```filter_kmers.sh```: Concatenates sample kmer counts for each kmer batch.
    - **Inputs**:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/<SAMPLE>/kmer_counts.<KMER_BATCH>.txt``` 
    - **Outputs**:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/unknown_alt_haplotype_kmers_filt.<KMER_BATCH>.tsv```,
    ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/kmers.filt.<KMER_BATCH>.tsv```
    
5.  ```concat_filtered_kmers.sh```: Concatenates sample kmer counts for each kmer batch.
    - **Inputs**:  ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/unknown_alt_haplotype_kmers_filt.<KMER_BATCH>.tsv```,
    ```../intermediate_files/unplaced_decoy_seqs/sample_kmer_matrix/kmers.filt.<KMER_BATCH>.tsv```
    - **Outputs**:  ```data/unplaced_decoy_seqs_kmer_counts.tsv```, ```data/unplaced_decoy_seqs_kmers.txt```