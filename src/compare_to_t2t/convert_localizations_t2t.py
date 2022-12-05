import pandas as pd
import numpy as np
import sys

localized = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_start_with_Y.bed', header=None)
localized_end = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_end_with_Y.bed', header=None)

localized.columns = ['chrom', 'start', 'NULL', 'idx']
localized.drop('NULL', axis=1, inplace=True)
localized['end'] = localized_end[1]
localized = localized[localized.chrom!='chr24']
localized['chrom'] = localized['chrom'].replace('chr23', 'chrX')

localized[['chrom', 'start', 'end', 'idx']].to_csv(
    '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_regions_hg38_for_conversion.bed',
    header=None, sep='\t', index=None)
print(len(localized))

