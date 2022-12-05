
import pandas as pd
import numpy as np

import sys

batch_number = int(sys.argv[1])
localized = pd.read_table('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_%04d.tsv' % batch_number, comment='#', header=None)
localized.index = 100000*batch_number+localized.index
localized = localized[~np.isnan(localized[6])][[6,7,8]]
localized['chrom'] = [('chr%i'% int(i)).replace('23', 'X') for i in localized[6]]
localized['start'] = [int(i) for i in localized[7]]
localized['end'] = [int(i) for i in localized[8]]
localized['index'] = localized.index
localized[['chrom', 'start', 'start', 'index']].to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_%04d_start_with_Y.bed' % batch_number,
                                                     header=None, index=None, sep='\t')
localized[['chrom', 'end', 'end', 'index']].to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_%04d_end_with_Y.bed' % batch_number,
                                                     header=None, index=None, sep='\t')

localized = localized[localized.chrom!='chr24']
localized[['chrom', 'start', 'start', 'index']].to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_%04d_start.bed' % batch_number,
                                                     header=None, index=None, sep='\t')
localized[['chrom', 'end', 'end', 'index']].to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_%04d_end.bed' % batch_number,
                                                     header=None, index=None, sep='\t')
print('saved to /home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/unmapped/localized_%04d.bed' % batch_number)