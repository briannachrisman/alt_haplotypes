import pandas as pd
import numpy as np

a = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_regions_T2T.bed', header=None)
a.columns = ['chrom', 'start', 'end', 'read_idx', 'alignment_idx']
a['length'] = -abs(a.end-a.start)
a.drop('alignment_idx', axis=1, inplace=True)
a = a.groupby(['read_idx', 'chrom']).aggregate(
    {'start': lambda x: (min(x), max(x)),
     'end': lambda x: (min(x), max(x)),
    'length': sum})
a = a.reset_index()
a.sort_values(['read_idx'])
a = a.sort_values(['read_idx', 'length'])
a = a[~a['read_idx'].duplicated()]
a.index = a.read_idx
a['start_true'] = np.min([a.start.apply(min).values, a.end.apply(min).values], axis=0)
a['end_true'] = np.max([a.start.apply(max).values, a.end.apply(max).values], axis=0)
a.drop(['start', 'end', 'read_idx', 'length'], axis=1, inplace=True)
a.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_regions_T2T_good_ids.bed', header=None, sep='\t')