# Localize

Scripts to localize k-mers to specific regions of the genome via a likelihood model.

## General Directory Structure

## Prerequisites

## Pipeline


1. ***CURRENTLY RUNNING***  ```build_family_probability_cache.sh```: Computes dictionaries of the log-likelihood that a family with phasings P has various k-mer count distributions. This dictionary will then be used to lookup probabilities in the likelihood model in order to speed up computation.
    - **Inputs**: ```alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle```, ```general_data/flagstat.csv```, ```general_data/bam_mappings.csv```
    - **Outputs**: ```alt_haplotypes/intermediate_files/localize/family_probability_cache_<PHASING_IDX>.pickle```
    
2. ```concat_family_probability_cache.sh```: This concatenates all of the family log-likelihoods into one large dictionary.
    - **Inputs**:  ```alt_haplotypes/intermediate_files/localize/family_probability_cache_<PHASING_IDX>.pickle```
    - **Outputs**:  ```alt_haplotypes/data/localize/family_probability_cache.pickle```

3. ```localize_<dataset>.sh```: Localize.

```localize_simulated_kmers.sh```: Compute likelihoods and localize
- **Inputs**:  ```alt_haplotypes/intermediate_files/localize/family_probability_cache_<PHASING_IDX>.pickle```
- **Outputs**:  ```alt_haplotypes/data/localize/family_probability_cache.pickle```

```localize_known_decoys.sh```: Compute likelihoods and localize 
- **Inputs**:  ```alt_haplotypes/intermediate_files/localize/family_probability_cache_<PHASING_IDX>.pickle```
- **Outputs**:  ```alt_haplotypes/data/localize/family_probability_cache.pickle```
    
```localize_unknown_decoys.sh```: Compute likelihoods and localize 
- **Inputs**:  ```alt_haplotypes/intermediate_files/localize/family_probability_cache_<PHASING_IDX>.pickle```
- **Outputs**:  ```alt_haplotypes/data/localize/family_probability_cache.pickle```
    
```localize_unmapped_reads.sh```: Compute likelihoods and localize 
- **Inputs**:  ```alt_haplotypes/intermediate_files/localize/family_probability_cache_<PHASING_IDX>.pickle```
- **Outputs**:  ```alt_haplotypes/data/localize/family_probability_cache.pickle``
    
    

