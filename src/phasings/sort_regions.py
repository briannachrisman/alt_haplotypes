import pandas as pd
df = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/regions.tsv',header=None)
df_sort = df.sort_values([0,1,2])
df_sort.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/regions_sorted.tsv',
               header=None, index=None, sep='\t')