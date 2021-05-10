import pandas as pd
import numpy as np
import sys 

FAMILY= sys.argv[1]
FINAL_PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams'
KELLEY_PHASINGS_DIR = '/oak/stanford/groups/dpwall/users/kpaskov/PhasingFamilies/phased_ihart.ms2_del'
df = pd.read_table('%s/%s.phased.txt' % (KELLEY_PHASINGS_DIR, FAMILY))

df.drop(['m1_del', 'm2_del', 'p1_del', 'p2_del', 'loss_region'], axis=1, inplace=True)
is_dup = False
prev_row = df.iloc[0][:-2]
start_idx = 0
idx_to_combine = []
for i,row in enumerate(df.iterrows()):
    if i==0: continue
    if (row[1][:-2]==prev_row).all():
        end_idx = i
        is_dup = True
    else:
        if is_dup:
            idx_to_combine = idx_to_combine + [(start_idx, end_idx)]
        is_dup = False
        start_idx = i
        prev_row = row[1][:-2]

# One last cycle through for last region of genome.
if is_dup:
    idx_to_combine = idx_to_combine + [(start_idx, end_idx)]
        
new_df = df.copy()
for start_idx, stop_idx in idx_to_combine:
    new_df.loc[start_idx,'end_pos']=new_df.iloc[stop_idx]['end_pos']
new_df = new_df.iloc[[i for i,_ in idx_to_combine]]     
new_df.to_csv('%s/%s.txt' % (FINAL_PHASINGS_DIR, FAMILY), sep='\t')
print(len(df), 'original rows')
print(len(new_df), 'rows in cleaned dataframe')
