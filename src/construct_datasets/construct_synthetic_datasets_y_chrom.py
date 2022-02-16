import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
import sys

REPEAT_AVG = int(sys.argv[1])
N = int(sys.argv[2])

np.random.seed(42)

# Load bam_mappings metadata file.
BAM_MAPPINGS_FILE = '/home/groups/dpwall/briannac/general_data/bam_mappings.csv'
bam_mappings = pd.read_csv(BAM_MAPPINGS_FILE, sep='\t', index_col=1)
bam_mappings = bam_mappings[bam_mappings['status']=='Passed_QC_analysis_ready']


# Load phasings information.
PHASINGS_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/'
OUT_DIR='/home/groups/dpwall/briannac/alt_haplotypes/data/counts/'

fam_idx_to_region = np.load(PHASINGS_DIR +  'idx_to_fam_region.npy', allow_pickle=True).item()
global_region_to_idx = np.load(PHASINGS_DIR +  'global_region_to_idx.npy', allow_pickle=True).item()
global_idx_to_fam_idx = np.load(PHASINGS_DIR + 'global_region_to_fam_regions.npy', allow_pickle=True)
family_info = pd.read_pickle(PHASINGS_DIR + 'fam_list.df')


# Get random locations.
locations = np.random.choice([list(global_region_to_idx.keys())[-1]], N, replace=True)
freqs = np.random.random(N)
location_idxs = [global_region_to_idx[l] for l in locations]
fam_regions = [[fam_idx_to_region[g] for g in global_idx_to_fam_idx[i]] for i in location_idxs]


# Save locations to file.
with open(OUT_DIR + 'synthetic_data_locations_y.txt', 'w') as f:
    for l,fr in zip(locations, freqs):
        f.writelines(l + '\t' + str(fr) + '\n')
        
        
# Get k-mer depth dictionary.
kmer_length=100
ihart_flagstat_file = '/home/groups/dpwall/briannac/blood_microbiome/data/ihart_flagstat.csv'
flagstat = pd.read_csv(ihart_flagstat_file, index_col=0)
flagstat = flagstat.loc[set(flagstat.index).intersection(bam_mappings.index)]
sex = bam_mappings.loc[flagstat.index].sex_numeric
total_mapped_reads = flagstat.ProperPair*((flagstat.Total_Reads-flagstat.Supplementary-flagstat.Duplicates)/flagstat.Total_Reads)
avg_coverage = total_mapped_reads*150/(6.27e9*(sex.astype(float)==1.0) + 6.37e9*(sex.astype(float)==2.0))
avg_n_100mers = (150-kmer_length)/(150/avg_coverage)
kmer_depth_dict = {k:avg_n_100mers[k] if k in avg_n_100mers else np.mean(avg_n_100mers.values) for k in bam_mappings.index}


with open('/home/groups/dpwall/briannac/alt_haplotypes/data/phasings/phased_fams/phased_fams_all.pickle', 'rb') as f:
    phased_fam_dict = pickle.load(f)
        
# Simulate k-mer counts.
print(REPEAT_AVG)
counts = pd.DataFrame()


for fam in tqdm(list(phased_fam_dict.keys())):
    if fam not in family_info.index: continue
    mother_sample = family_info.loc[fam].mother_sample
    father_sample = family_info.loc[fam].father_sample
    children_samples = family_info.loc[fam].sib_samples

    current_fam_regions = [set(f).intersection(phased_fam_dict[fam].index) for f in fam_regions]
    current_fam_regions = [list(c)[0] if len(c)==1 else np.random.choice(phased_fam_dict[fam].index) for c in current_fam_regions]
    phased_fam = phased_fam_dict[fam].loc[current_fam_regions][children_samples].values
    phased_fam = np.array([[(p[0]%4, p[1]%4) for p in pp] for pp in phased_fam])
        
    if REPEAT_AVG == 1:
        mom_g1 = (np.random.random(N)<=freqs)*1
        dad_g1 = (np.random.random(N)<=freqs)*1
        mom_g2 = (np.random.random(N)<=freqs)*1
        dad_g2 = (np.random.random(N)<=freqs)*1
    else:
        mom_g1 = (np.random.random(N)<=freqs)*np.random.poisson(REPEAT_AVG, N)
        dad_g1 = (np.random.random(N)<=freqs)*np.random.poisson(REPEAT_AVG, N)
        mom_g2 = (np.random.random(N)<=freqs)*np.random.poisson(REPEAT_AVG, N)
        dad_g2 = (np.random.random(N)<=freqs)*np.random.poisson(REPEAT_AVG, N)

    # Correct for X and Y chromsomes.
    dad_g2 = [0 if 'X' in r else g for g,r in zip(dad_g2, current_fam_regions)]
    mom_g1 = [0 if 'Y' in r else g for g,r in zip(mom_g1, current_fam_regions)]
    mom_g2 = [0 if 'Y' in r else g for g,r in zip(mom_g2, current_fam_regions)]
    dad_g1 = [0 if 'Y' in r else g for g,r in zip(dad_g1, current_fam_regions)]
        
        
        # Simulate parent's genotypes based on phasing and simulated info about sequence.
    mom_gts = np.array([mom_g1, mom_g2]).transpose()
    dad_gts = np.array([dad_g1, dad_g2]).transpose()

    # Simulate counts based on genotype and phasing.
    mom_counts = mom_g1*np.random.poisson(kmer_depth_dict[mother_sample], N)+mom_g2*np.random.poisson(kmer_depth_dict[mother_sample], N)
    dad_counts = dad_g1*np.random.poisson(kmer_depth_dict[mother_sample], N)+dad_g2*np.random.poisson(kmer_depth_dict[mother_sample], N)
    children_counts = [[np.random.poisson(
        kmer_depth_dict[children_samples[ch_idx]]) * 
        (mom_gts[region_idx,phased_fam[region_idx, ch_idx][0]] + 
         dad_gts[region_idx,phased_fam[region_idx, ch_idx][1]])
                        for ch_idx in range(phased_fam.shape[1])] for region_idx in range(phased_fam.shape[0])]

    # Update total dataframe
    counts[mother_sample] = mom_counts
    counts[father_sample] = dad_counts
    for c_i, c in enumerate(children_samples):
        counts[c] = [children_count[c_i] for children_count in children_counts]
            
counts.to_csv(OUT_DIR + 'synthetic_data_y_chrom_%i_repeats.tsv' % REPEAT_AVG, sep='\t', header=counts.columns, index=None)
    
    
