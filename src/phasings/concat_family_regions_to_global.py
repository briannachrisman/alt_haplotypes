# Combine all dictionaries.
import numpy as np

FINAL_PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings'
PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/phasings'
family_region_to_global_regions_chom_all = np.array([])
for chrom in range(1,24):
    print(chrom)
    if chrom==23:
        family_region_to_global_regions_chom_all = np.append(
            family_region_to_global_regions_chom_all,
            np.load(PHASINGS_DIR + '/fam_regions_to_global_region_X.npy', allow_pickle=True))
    else:
        family_region_to_global_regions_chom_all = np.append(
            family_region_to_global_regions_chom_all,
            np.load(PHASINGS_DIR + '/fam_regions_to_global_region_%i.npy' % chrom, allow_pickle=True))
np.save(FINAL_PHASINGS_DIR + '/fam_regions_to_global_regions.npy', family_region_to_global_regions_chom_all)