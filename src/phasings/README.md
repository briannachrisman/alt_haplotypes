# Phasings
Computes dictionaries, mappings, etc. related to phasings. To be used in later in alternative haplotype localizing.

## Storage
**Intermediate data**: ```/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/phasings```
**Final data**:  ```/home/groups/dpwall/briannac/alt_haplotypes/data/phasings```

***Note: Not archiving any of this, as it did not take too long to run.***

## Prerequisites

0.1. ✓ Get Kelley to phase ihart. (Stored in ```/oak/stanford/groups/dpwall/users/kpaskov/PhasingFamilies/phased_ihart.ms2_del```) 

## Pipeline

1. ✓ ```clean_phasing.sh ```: Clean phasings to get rid of "deletion" rows. 
    - **inputs**: ```/oak/stanford/groups/dpwall/users/kpaskov/PhasingFamilies/phased_ihart.ms2_del/<FAMILY>.txt```
    - **outputs**: ```data/phasings/phased_fams/<FAMILY>.txt```

1. ✓ ```add_y_chromsome.ipynb ```: Adds Y-chromosome row.
    - **inputs**: ```data/phasings/phased_fams/<FAMILY>.txt```
    - **outputs**: ```data/phasings/phased_fams/<FAMILY>_with_y.txt```

3. ✓ ```extract_phasing_regions.sh```: Extracts a list of all phasing regions. 
    - **input**s: ```data/phasings/phased_fams/<FAMILY>_with_y.txt```
    - **outputs**: ```intermediate_files/phasings/regions.tsv```

4. ✓ ```list_of_global_and_family_regions.py```: Create data frames of family regions, start/stop/chrom, dict of global region to idx and vice versa, dict of family region to idx and vice versa. 
    - **inputs**: ```intermediate_files/phasings/regions.tsv```
    - **outputs**: ```data/phasings/family_regions.df```, ```starts_stops_chrom.df```, ```idx_to_global_region.npy```, ```global_region_to_idx.npy```, ``idx_to_family_region.npy```, ```family_region_to_idx.npy```


5. ✓ ```family_regions_to_global.sh```: For each chromsome, creates a dictionary to convert family region idx to global region(s) idx(s). 
    IE family region dict_chr1[10]=100,101,102
    - **inputs**: ```intermediate_files/phasings/global_region_to_idx.npy```, ```fam_region_to_idx.npy```, ```starts_stops_chrom.npy```, ```family_regions.npy```
    - **outputs**: ```intermediate_files/phasings/fam_regions_to_global_region_[chrom].npy```

6. ✓ ```concat_family_regions_to_global.sh```: Concatenates individual chromosomal dictionaries family_region_to_global_region_chr%i.npy to genome-wide dictionary.  
    - **inputs** ```intermediate_files/phasings/fam_regions_to_global_region_[chrom].npy```
    - **outputs** ```data/phasings/fam_regions_to_global_region.npy```