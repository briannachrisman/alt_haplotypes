# Run with python3.6 -u $MY_HOME/alt_haplotypes/src/phasings/family_phasing_dictionary.py

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
fam_region_to_idx = np.load(PHASINGS_DIR +  'fam_region_to_idx.npy', allow_pickle=True).item()
idx_to_fam_region = np.load(PHASINGS_DIR +  'idx_to_fam_region.npy', allow_pickle=True).item()
global_region_to_idx = np.load(PHASINGS_DIR +  'global_region_to_idx.npy', allow_pickle=True).item()
idx_to_global_region = np.load(PHASINGS_DIR +  'idx_to_global_region.npy', allow_pickle=True).item()
fam_idx_to_global_idx = np.load(PHASINGS_DIR + 'fam_regions_to_global_regions.npy', allow_pickle=True)
family_info = pd.read_pickle(PHASINGS_DIR + 'fam_list.df')

# Info from BAM mappings.
bam_mappings = pd.read_csv(BAM_MAPPINGS_FILE, sep='\t', index_col=1)
bam_mappings = bam_mappings[bam_mappings['status']=='Passed_QC_analysis_ready']

families_in_file = list(set(family_info.index).intersection([i.replace('.txt', '').split('/')[-1] for i in glob(
            '/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/*.txt')]))
print(len(families_in_file))
phased_fam_dict = dict()
for fam in families_in_file:
    print(fam)
    sample_id_to_participant = {sample_id:participant_id for participant_id, sample_id in zip(bam_mappings.participant_id, bam_mappings.index)}

    # Extract mom, dad, and child sample_ids.
    children = family_info.loc[fam].sib_samples
    mom = family_info.loc[fam].mother_sample
    dad = family_info.loc[fam].father_sample
    phased_fam = pd.read_csv('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/%s.txt' % fam,
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
        phased_fam.index = ['%s.%09d.%09d' % (('0' + chrom[3:])[-2:].replace('0X', 'XX'), start, end) for chrom, start, end in phased_fam[['chrom', 'start_pos', 'end_pos']].values]
    phased_fam_dict[fam] = phased_fam[children]
    
with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'wb') as f:
    pickle.dump(phased_fam_dict, f, protocol=pickle.HIGHEST_PROTOCOL)