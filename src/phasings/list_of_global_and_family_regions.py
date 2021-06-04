# Load in phased regions.
import pandas as pd
import numpy as np

PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings'
FINAL_PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings'

# Find all family regions.

### Note: For some reason, family_regions.df and starts_stops_chrom.df save funny
### if run in script, but work ok if run in python notebook...
print('building family regions dataframe...')
start_ends = pd.read_table(PHASINGS_DIR + '/regions.tsv', header=None)

start_ends.columns = ['chrom', 'start_pos', 'end_pos']
start_ends['chrom']  = [c.replace('chr', '') for c in start_ends['chrom']]
#start_ends['chrom']  = [c.replace('X', 'XX') for c in start_ends['chrom']]
#start_ends['chrom']  = ['0' + c if len(c)==1 else c for c in start_ends['chrom']]
start_ends['start_pos']  = [int(c) for c in start_ends['start_pos']]
start_ends['end_pos']  = [int(c) for c in start_ends['end_pos']]
start_ends.sort_values(['chrom', 'start_pos', 'end_pos'], inplace=True)
start_ends.index = ['%s.%09d.%09d' % (i,int(j),int(k)) for i,j,k in zip(start_ends.chrom, start_ends.start_pos, start_ends.end_pos)]
start_ends.to_pickle(FINAL_PHASINGS_DIR + '/family_regions.df')

# Find all start/ends for global regions.
print("Building grouped dataframe...")
grouped = start_ends.groupby('chrom').aggregate(lambda x: sorted(list(set(x))))
grouped['positions'] = [sorted(list(set(g[1].start_pos).union(set(g[1].end_pos)))) for g in grouped.iterrows()]
grouped['starts'] = [g[1].positions[:-1] for g in grouped.iterrows()]
grouped['ends'] = [g[1].positions[1:] for g in grouped.iterrows()]
grouped.drop(['start_pos', 'end_pos', 'positions'], axis=1, inplace=True)
grouped.to_pickle(FINAL_PHASINGS_DIR + '/starts_stops_chrom.df')

# Create dictionary of family region / index.
print('building dictionary of family regions/idx...')
fam_region_to_idx = {i:j for i,j in zip(start_ends.index, list(range(len(start_ends))))}
idx_to_fam_region = {j:i for i,j in zip(start_ends.index, list(range(len(start_ends))))}
np.save(FINAL_PHASINGS_DIR + '/fam_region_to_idx.npy', fam_region_to_idx)
np.save(FINAL_PHASINGS_DIR + '/idx_to_fam_region.npy', idx_to_fam_region)

# Create dictionary of global region / index
print('building dictionary of global regions/idx...')
global_regions = ['%s.%09d.%09d' % (i[0], i[1].starts[s], i[1].ends[s]) for i in grouped.iterrows() for s in range(len(i[1].starts))]
idx_to_global_region = {i:region for i,region in enumerate(global_regions)}
global_region_to_idx = {region:i for i,region in enumerate(global_regions)}
np.save(FINAL_PHASINGS_DIR + '/idx_to_global_region.npy', idx_to_global_region)
np.save(FINAL_PHASINGS_DIR + '/global_region_to_idx.npy', global_region_to_idx)


