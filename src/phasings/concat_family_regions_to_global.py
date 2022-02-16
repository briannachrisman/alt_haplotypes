# Combine all dictionaries.
import numpy as np
import pandas as pd

FINAL_PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings'
PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/phasings'
family_region_to_global_regions_chrom_all = np.array([])
for chrom in range(1,25):
    print(chrom)
    if chrom==23:
        family_region_to_global_regions_chrom_all = np.append(
            family_region_to_global_regions_chrom_all,
            np.load(PHASINGS_DIR + '/fam_regions_to_global_region_XX.npy', allow_pickle=True))
    elif chrom==24:
        family_region_to_global_regions_chrom_all = np.append(
            family_region_to_global_regions_chrom_all, 
            np.load(PHASINGS_DIR + '/fam_regions_to_global_region_YY.npy', allow_pickle=True))
        family_region_to_global_regions_chrom_all[-1] = [family_region_to_global_regions_chrom_all[-1]]
    else:
        family_region_to_global_regions_chrom_all = np.append(
            family_region_to_global_regions_chrom_all,
            np.load(PHASINGS_DIR + '/fam_regions_to_global_region_%02d.npy' % chrom, allow_pickle=True))

np.save(FINAL_PHASINGS_DIR + '/fam_regions_to_global_regions.npy', family_region_to_global_regions_chrom_all)



idx_to_global_region = np.load(FINAL_PHASINGS_DIR +  '/idx_to_global_region.npy', allow_pickle=True).item()
print(len(idx_to_global_region))
global_region_to_fam_region = [[] for i in idx_to_global_region]
for f, global_regions in enumerate(family_region_to_global_regions_chrom_all):
    for g in global_regions:
        global_region_to_fam_region[g] = global_region_to_fam_region[g] + [f]

np.save(FINAL_PHASINGS_DIR + '/global_region_to_fam_regions.npy', global_region_to_fam_region)