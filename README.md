This repository contains the code and analysis for ASLAN, an Algorithm for Sequence Localition Approximation using Nuclear families, as described in [https://www.biorxiv.org/content/10.1101/2022.08.02.502486v1](https://www.biorxiv.org/content/10.1101/2022.08.02.502486v1).

ASLAN's goal is to localize k-mers from reads that failed to map to a human reference genome, either because they come from genetically diverse regions not well-represented on the current reference genome,  or they come from parts of the genome that are gapped in the current human reference genome (heterochromatin).

ASLAN uses **phasings of siblings** (which chromsomal regions children share maternally and paternally) and (2) a **distribution of k-mers extracted from unmapped reads** in whole genome sequences in order to build a maximum likelihood model that determines the most likely genomic region a k-mer originates from. 

# Data and Results

## iHART Raw Data

The raw reads from the iHART samples can be found on Anvil, maintained by NHGRI at \texttt{https://anvilproject.org/data/studies/phs001766}. Dataset access is controlled in adherence to NIH Policy and in line with the standards set forth in the individual consents involved in each cohort.

Information on the sample collection process, alignment, and quality control is described 

    Ruzzo, Elizabeth K., et al. "Inherited and de novo genetic risk for autism impacts shared networks." Cell 178.4 (2019): 850-866. https://doi.org/10.1016/j.cell.2019.07.015

## Results of ASLAN

We provide the results of ASLAN on the unmapped reads from the iHART dataset, along with the corresponding T2T alignments. These files can be found under '''results/public_data''' The directory contains 3 files:

* '''ASLAN_localizations.bed''': A .bed file containing the chromosome, start coordinate, end coordinate, and k-mer index (starting from 0) of the region ASLAN localized each k-mer to. Coordinates are in the GRCh38 system. 
* '''T2T_mappings.bed''': A .bed file containing the chromosome, start coordinate, end coordinate, and k-mer index (starting from 0) of each k-mer's primary alignment to the T2T-CHM13 reference. Coordinates have been translated to the GRCh38 system.
* '''kmers.txt.zip''': A compressed list of k-mer extracted from the unmapped reads. The order of these k-mers corresponds to the k-mer index in the previously described .bed files.


# ASLAN Pipeline

ASLAN requires a very specific dataset, a large data set of nuclear families with multiple children. We used ASLAN on unmapped reads extracted from the iHART dataset. To our knowledge, this is the only family dataset large enough for ASLAN to work with. Nevertheless, we describe the ASLAN pipeline and the code for running it, for those who may be able to use the ASLAN pipeline on data with similar characteristics to iHART, or to modify the ASLAN pipeline to work on their own uniquely structured sequencing dataset.

## Phasings

In this case, genetic phasings refers to the regions of shared (maternal and paternal) genetic material between siblings. Our algorithm requires a matrix of siblings x chromsomal regions and information about which copy of maternal (0 or 1) and paternal chromsome (2 or 3) a child inherited at a given region. The regions should be separated at each computed recombination point.


An example of a phasing matrix would look as follows:

chrom   start      stop        ch1_mat       ch1_pat     ch2_mat     ch2_pat     ch3_mat     ch3_pat...
1       0          25000        0 or 1       2 or 3      0 or 1       2 or 3      0 or 1     2 or 3...   
1       25001     30000009      0 or 1       2 or 3      0 or 1       2 or 3      0 or 1     2 or 3...  


We used an in-house algorithm to generate these phasings, that uses variant calls from WGS of families. Other options for various structures of datasets are described in:
   
    Choi, Yongwook, et al. "Comparison of phasing strategies for whole human genomes." PLoS genetics 14.4 (2018): e1007308. https://doi.org/10.1371/journal.pgen.1007308
    
    Roach, Jared C., et al. "Chromosomal haplotypes by genetic phasing of human families." The American Journal of Human Genetics 89.3 (2011): 382-397. https://doi.org/10.1016/j.ajhg.2011.07.023
    
    
    Browning, Sharon R., and Brian L. Browning. "Haplotype phasing: existing methods and new developments." Nature Reviews Genetics 12.10 (2011): 703-714. https://doi.org/10.1038%2Fnrg3054
    
       
       
To clean up the phasings and create a global dictionary (containing all families) of phasings, the following need to be run:

The scripts can be found within ```src/phasings/```

1.  ```clean_phasing.sh ```: (Optional, if phasings include deletions/insertions). Clean phasings to get rid of "deletion" rows. 
    - **inputs**: Family phasing files - ```<FAMILY>.txt```
    - **outputs**: Cleaned phasing file - ```<FAMILY>_phased.txt```

2.  ```add_y_chromsome.ipynb ```: Adds a dummy row for the Y-chromosome row, which always has the same phasing (sons inherit full chromsome from father).
    - **inputs**: ```<FAMILY>_phased.txt```
    - **outputs**: Family phasing file with Y - ```<FAMILY>_with_y.txt```

3.  ```extract_phasing_regions.sh```: Extracts a list of all of the possible phasing regions (recombination points) across all families. 
    - **input**s: ```<FAMILY>_with_y.txt```
    - **outputs**: List of regions and which families have recombination points at a given region - ```regions.tsv```

4.  ```list_of_global_and_family_regions.py```: Create data frames of family regions, start/stop/chrom, dict of global region to idx and vice versa, dict of family region to idx and vice versa. 
    - **inputs**: L```intermediate_files/phasings/regions.tsv```
    - **outputs**: Dataframes and arrays describing the the identities of different regions - ```data/phasings/family_regions.df```, ```starts_stops_chrom.df```, ```idx_to_global_region.npy```, ```global_region_to_idx.npy```, ``idx_to_family_region.npy```, ```family_region_to_idx.npy```


5.  ```family_regions_to_global.sh```: For each chromsome, creates a dictionary to convert family region idx to global region(s) idx(s). 
    IE family region dict_chr1[10]=100,101,102
    - **inputs**: ```intermediate_files/phasings/global_region_to_idx.npy```, ```fam_region_to_idx.npy```, ```starts_stops_chrom.npy```, ```family_regions.npy```
    - **outputs**: Numpy array describing where each region within a family falls according to the global index - ```fam_regions_to_global_region_[chrom].npy```

6.  ```concat_family_regions_to_global.sh```: Concatenates individual chromosomal dictionaries family_region_to_global_region_chr%i.npy to genome-wide dictionary.  
    - **inputs** ```fam_regions_to_global_region_[chrom].npy```
    - **outputs** Dictionary/numpy array converting family region index (0, 1, 2, 3...) to global index - ```fam_regions_to_global_region.npy```

## K-mer Extraction and Counts

ASLAN also requires counts of various k-mers you are interested in localizing. Extracting and counting k-mers from large sets of reads can be computationally costly, so we recommend using highly optimized and parallelized. We used [```jellyfish```](https://github.com/gmarcais/Jellyfish)

We used ```jellyfish count``` to count the k-mers in each individual's unmapped reads, ```jellyfish merge``` to compute the list of all k-mers in the collection of unmapped reads, and ```jellyfish query``` to then query the count of each k-mer in each individual's unmapped reads.  The result is 
(1) A list of all of the k-mers in all of the individuals.
(2) A matrix of k-mers x individuals with the number of times a specific k-mer occured in the reads of each individual. 

More information on jellyfish can be found at:

    Marçais, Guillaume, and Carl Kingsford. "A fast, lock-free approach for efficient parallel counting of occurrences of k-mers." Bioinformatics 27.6 (2011): 764-770.


## Maximum Likelihood Model

The maximum likelihood


1. ```family_likelihoods.sh```: For each family, computes (1) a matrix of Likelihoods with possible phasings for rows x kmers for columns and (2) a presence/absence matrix with possible phasings as rows and global regions as columns.
    - **Inputs**: Phasing and k-mer information produced by the previous steps - ```kmers.txt```, ```kmer_counts.tsv```, ```global_region_to_idx.npy```, ```fam_regions_to_global_regions.npy```, ```fam_region_to_idx.npy```
    - **Outputs**:  Family-level information about the phasings at each region, and the likelihood of a given k-mer for each phasing combination of a family - ```likelihood_matrix_phasings_kmers_fam<FAM_NUM>.tsv```, ```global_regions_phasings_fam<FAM_NUM>.tsv```, 


2. ```concat_family_likelihoods.sh```: Concatenates lengthwise the outputs from ```family_likelihoods.sh``` to get (1) (1) a matrix of Likelihoods with kmers for rows x each family's possible phasings for columns and (2) a presence/absence matrix with each global regions as rows and family's possible phasings as columns.
    - **Inputs**:  ```likelihood_matrix_phasings_kmers_fam<FAM_NUM>.tsv```, ```global_regions_phasings_fam<FAM_NUM>.tsv```
    - **Outputs**:  Concatenated likelihood matrix across all families, and a sparse matrix describing the phasings of each family at each region -```likelihood_matrix_phasings_kmers.tsv```, ```global_regions_phasings.tsv```


3. ```localize.sh```: For each block of k-mers, find region of maximum/sufficient likelihood.
    - **Inputs**: ```likelihood_matrix_phasings_kmers.tsv```, ```global_regions_phasings.tsv```
    - **Outputs**: A list of maximum likelihood given the cutoff threshold for each batch of k-mers - ```approximate_region_<KMER_IDX>.txt```


4. ```concat_region_approximations.sh```: Concatenate localized regions for all kmers.
    - **Inputs**: ```approximate_region_<KMER_IDX>.txt```
    - **Outputs**: A concatenated list of approximate regions for each k-mer given the tuning threshold - ```approximate_regions.tsv```


## Additional Analysis and Benchmarking Scripts

Source code for benchmarking the algorithm on simulated and decoy datasets can be found under ```/src/simulated_k_counts/``` and ```/src/unplaced_decoy_seqs/``` and the corresponding figures found at ```/src/figures```


Source code for analyzing ASLAN's performance against alignment to the CHM13-T2T in order to understand discrepancies and hotspots for genetic diversity can be found at ```/src/compare_to_t2t/```.

