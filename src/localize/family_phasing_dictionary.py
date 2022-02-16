# Run with python3.6 -u $MY_HOME/alt_haplotypes/src/localize/family_phasing_dictionary.py

import time
import pandas as pd
import numpy as np
from tqdm import tqdm
from glob import glob
import pickle 

PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/'
BAM_MAPPINGS_FILE = '/home/groups/dpwall/briannac/general_data/bam_mappings.csv'
KMER_COUNTS_FILE = '/home/groups/dpwall/briannac/alt_haplotypes/results/simulated_data/kmer_counts.tsv'

# Load in family region/global region conversion data.
family_info = pd.read_pickle(PHASINGS_DIR + 'fam_list.df')

# Info from BAM mappings.
bam_mappings = pd.read_csv(BAM_MAPPINGS_FILE, sep='\t', index_col=1)
bam_mappings = bam_mappings[bam_mappings['status']=='Passed_QC_analysis_ready']

families_in_file = list(set(family_info.index).intersection([i.replace('_with_y.txt', '').split('/')[-1] for i in glob(
            '/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/*_with_y.txt')]))
print(len(families_in_file))
phased_fam_dict = dict()
for fam in families_in_file:
    print(fam)
    sample_id_to_participant = {sample_id:participant_id for participant_id, sample_id in zip(bam_mappings.participant_id, bam_mappings.index)}

    # Extract mom, dad, and child sample_ids.
    children = family_info.loc[fam].sib_samples
    mom = family_info.loc[fam].mother_sample
    dad = family_info.loc[fam].father_sample
    phased_fam = pd.read_csv('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/%s_with_y.txt' % fam,
                                     sep='\t')

    # Skip family if dataframe is weird.
    missing_children=False
    for ch in children:
        if sample_id_to_participant[ch] + '_mat' not in phased_fam.columns: 
            missing_children=True
            break
    if missing_children: continue
                
    # Set up phasing dataframe.
    for ch in children:
        phased_fam[ch] = [(m,d-2) for m,d in zip(phased_fam[sample_id_to_participant[ch]+'_mat'], phased_fam[sample_id_to_participant[ch]+'_pat'])]
        phased_fam.index = ['%s.%09d.%09d' % (('0' + chrom[3:])[-2:].replace('0X', 'XX').replace('0Y', 'YY').replace('0P', 'PP'), start, end) for chrom, start, end in phased_fam[['chrom', 'start_pos', 'end_pos']].values]
        
    # Correct for sex chromsomes.
    for child in children:
        if bam_mappings.loc[child].sex_numeric=='1.0':
            phased_fam[child] = [(i,5) if j==4 else (i,j) for i,j in phased_fam[child].values]
        if bam_mappings.loc[child].sex_numeric=='2.0':
            phased_fam[child] = [(i,4) if j==5 else (i,j) for i,j in phased_fam[child].values]

        
    phased_fam_dict[fam] = phased_fam[children]

with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'wb') as f:
    pickle.dump(phased_fam_dict, f, protocol=pickle.HIGHEST_PROTOCOL)