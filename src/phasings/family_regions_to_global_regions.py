# Load in phased regions.
import pandas as pd
import numpy as np
import sys
import json
import tqdm

chrom = str(sys.argv[1])
PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/phasings'
FINAL_PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings'

print(chrom)

print('loading dataframes and dicts...')
global_region_to_idx = np.load(FINAL_PHASINGS_DIR + '/global_region_to_idx.npy', allow_pickle=True).item()
family_region_to_idx = np.load(FINAL_PHASINGS_DIR + '/fam_region_to_idx.npy', allow_pickle=True).item()
grouped = pd.read_pickle(FINAL_PHASINGS_DIR + '/starts_stops_chrom.df')
start_ends = pd.read_pickle(FINAL_PHASINGS_DIR + '/family_regions.df')



print('loading dataframes and dicts...')
global_region_to_idx = np.load(FINAL_PHASINGS_DIR + '/global_region_to_idx.npy', allow_pickle=True).item()
family_region_to_idx = np.load(FINAL_PHASINGS_DIR + '/fam_region_to_idx.npy', allow_pickle=True).item()
grouped = pd.read_pickle(FINAL_PHASINGS_DIR + '/starts_stops_chrom.df')
start_ends = pd.read_pickle(FINAL_PHASINGS_DIR + '/family_regions.df')


print('computing contained regions...')
start_pos_global = np.array(grouped.loc[chrom].starts)
end_pos_global = np.array(grouped.loc[chrom].ends)
start_ends_chrom = start_ends[start_ends['chrom']==chrom]
start_pos_family = start_ends_chrom.start_pos.values
end_pos_family = start_ends_chrom.end_pos.values
contains_start = np.less_equal.outer(start_pos_family, start_pos_global)
contains_end = np.greater_equal.outer(end_pos_family, end_pos_global)
contains = contains_start & contains_end


print('building list...')
family_region_to_global_regions_list = [[] for i in range(len(start_pos_family))]
for i in tqdm.tqdm(range(len(start_pos_family))):
    family_region_to_global_regions_list[i] = [
        global_region_to_idx['%s.%09d.%09d' % (chrom, start_pos_global[s], end_pos_global[s])] for s in np.where(contains[i])[0]]

print('saving...')
np.save(PHASINGS_DIR + '/fam_regions_to_global_region_%s.npy' % chrom, np.array(family_region_to_global_regions_list))

