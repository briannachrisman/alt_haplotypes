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


print('computing contained regions...')
start_pos = np.array(grouped.loc[chrom].starts)
end_pos = np.array(grouped.loc[chrom].ends)
start_ends_chrom = start_ends[start_ends['chrom']==chrom]
contains_start = np.less_equal.outer(start_ends_chrom.start_pos.values, start_pos)
contains_end = np.greater_equal.outer(start_ends_chrom.end_pos.values, end_pos)
contains = contains_start & contains_end


print('building list...')
family_region_to_global_regions_list = [[] for i in range(len(contains))]
for i in tqdm.tqdm(range(len(contains))):
    family_region_to_global_regions_list[i] = [
        global_region_to_idx['%s.%i.%i' % (chrom, start_pos[s], end_pos[s])] for s in np.where(contains[i])[0]]

print('saving...')
np.save(PHASINGS_DIR + '/fam_regions_to_global_region_%s.npy' % chrom, np.array(family_region_to_global_regions_list))