# Localize

Scripts to localize k-mers to specific regions of the genome via a likelihood model.

## General Directory Structure

## Prerequisites

## Pipeline

1 .```family_phasing_dictionary.py```

1. ```family_likelihoods.sh```: For each family, computes (1) a matrix of Likelihoods with possible phasings for rows x kmers for columns and (2) a presence/absence matrix with possible phasings as rows and global regions as columns.
    - **Inputs**: ```data/<ground_truth|unplaced_decoy_seqs|unmapped>_kmers.txt```, ```data/<ground_truth|unplaced_decoy_seqs|unmapped>_kmer_counts.tsv```
    - **Outputs**:  ```intermediate_files/family_likelihoods/<ground truth|unplaced_decoy_seqs|unmapped>/likelihood_matrix_phasings_kmers_fam<FAM_NUM>.tsv```, ```intermediate_files/family_likelihoods/<ground truth|unknown_kmers|unplaced_decoy_seqs>/global_regions_phasings_fam<FAM_NUM>.tsv```


2. ```concat_family_likelihoods.sh```: Concatenates lengthwise the outputs from ```family_likelihoods.sh``` to get (1) (1) a matrix of Likelihoods with kmers for rows x each family's possible phasings for columns and (2) a presence/absence matrix with each global regions as rows and family's possible phasings as columns.
    - **Inputs**:  ```intermediate_files/family_likelihoods/<ground truth|unplaced_decoy_seqs|unmapped>/likelihood_matrix_phasings_kmers_fam<FAM_NUM>.tsv```, ```intermediate_files/family_likelihoods/<ground truth|unknown_kmers|unplaced_decoy_seqs>/global_regions_phasings_fam<FAM_NUM>.tsv```
    - **Outputs**:  ```intermediate_files/family_likelihoods/<ground_truth|unknown_kmers|unmapped>/likelihood_matrix_phasings_kmers.tsv```, ```intermediate_files/family_likelihoods/<ground_truth|unknown_kmers|unmapped>/global_regions_phasings.tsv```


3. ```localize_<TYPE>.sh```: For each block of k-mers, find region of maximum/sufficient likelihood.
    - **Inputs**: ```intermediate_files/family_likelihoods/<ground truth|unknown_kmers|unmapped>_likelihood_matrix_phasings_kmers.tsv```, ```intermediate_files/family_likelihoods/<ground truth|unknown_kmers|unmapped>_global_regions_phasings.tsv```
    - **Outputs**: ```intermediate_files/localize/<ground truth|unknown_kmers|unmapped>/localized/n_<KMER_IDX>.txt```


4. ```concat_region_approximations.sh```: Concatenate localized regions for all kmers.
    - **Inputs**: ```intermediate_files/localize/<ground truth|unknown_kmers|unmapped>_approximate_region_<KMER_IDX>.txt```
    - **Outputs**: ```results/approximate_regions/localized_<ground truth|unknown_kmers|unmapped>.tsv```

