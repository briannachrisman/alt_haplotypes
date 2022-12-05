import pandas as pd
import sys
import numpy as np
import tqdm
import scipy.stats as stats
import matplotlib.pyplot as plt

N_BATCH = int(sys.argv[1])


bam_mappings = pd.read_table('/home/groups/dpwall/briannac/general_data/bam_mappings.csv', index_col=1)
bam_mappings = bam_mappings[bam_mappings.status=='Passed_QC_analysis_ready']
bam_mappings = bam_mappings.drop('09C86428')

##### Sex association ####
# Get pairings.
if True:
    print("Getting pairings...")
    samples = bam_mappings.index
    affected_pairs = []
    unaffected_pairs = []
    for f in set(bam_mappings.family):
        fam = bam_mappings[(bam_mappings.family==f) & (bam_mappings.relationship=='sibling')]
        #random
        #sex_numeric = fam.sex_numeric.copy()
        #np.random.shuffle(sex_numeric)
        #fam.sex_numeric = sex_numeric
        affected_females = fam[(fam.sex_numeric=='2.0') & (fam.derived_affected_status=='autism')]
        affected_males = fam[(fam.sex_numeric=='1.0') & (fam.derived_affected_status=='autism')]
        unaffected_females = fam[(fam.sex_numeric=='2.0') & (pd.isna(fam.derived_affected_status))]
        unaffected_males = fam[(fam.sex_numeric=='1.0') & (pd.isna(fam.derived_affected_status))]

        affected_pairs = affected_pairs + [(i,j) for i in affected_females.index for j in affected_males.index if ((i in samples) and (j in samples))]
        unaffected_pairs = unaffected_pairs + [(i,j) for i in unaffected_females.index for j in unaffected_males.index if ((i in samples) and (j in samples))]
    males = [m for f,m in (affected_pairs + unaffected_pairs)]
    females = [f for f,m in (affected_pairs + unaffected_pairs)]    


    pvals = np.zeros(100000) + np.nan
    effect_size = np.zeros(100000) + np.nan
    eps = 1e-20
    mult = 1.0159 #6.37/6.27 #p.median(covs[males].values.flatten())/np.median(covs[females].values.flatten())
    file = '/home/groups/dpwall/briannac/alt_haplotypes/data/kmers_unmapped_counts_filt.tsv'
    sig_covs_vcf = pd.DataFrame()
    for covs in pd.read_table(file, chunksize=1000, nrows=len(pvals), skiprows=N_BATCH*len(pvals), header=None, index_col=None):
        print(covs.index[0])
        covs.drop(0, inplace=True, axis=1)
        covs.columns = list(bam_mappings.index)
        covs_norm = covs[abs(covs[males].values-covs[females].values).sum(axis=1)>0]
        pvals[covs_norm.index] = [stats.wilcoxon(q[1][males]+eps, mult*q[1][females]+eps, zero_method='pratt', alternative='greater').pvalue for q in covs_norm.iterrows()]
        effect_size[covs_norm.index] = [sum(q[1][males].values >= mult*q[1][females].values)/sum(mult*q[1][females].values >= q[1][males].values) for q in covs_norm.iterrows()]
        sig_covs_vcf = pd.concat([sig_covs_vcf, covs_norm[(.5-abs(.5-pvals[covs_norm.index]))<(.05/10000000)]])
    pvals_sex = np.array([2*min(p, 1-p) for p in pvals])
    idx = np.array([i for i,p in enumerate(pvals_sex) if ~np.isnan(p)])
    effect_size_sex=np.array(effect_size)
    effect_size_sex = effect_size_sex[~np.isnan(pvals_sex)]
    pvals_sex = pvals_sex[~np.isnan(pvals_sex)]
    df = pd.DataFrame([pvals_sex, effect_size_sex], columns=idx).transpose()
    df.index = df.index + N_BATCH*len(pvals)
    df.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/pvals_sex/pvals_sex_%04d.tsv' % N_BATCH, sep='\t', header=None)
    sig_covs_vcf.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/sig_covs_sex/sig_covs_sex_%04d.tsv' % N_BATCH, sep='\t', header=None)

    
#### ASD Association ####
if False:
    print ("setting up ")
    # Set up dataframe to save.    
    samples = bam_mappings.index
    male_pairs = []
    female_pairs = []
    for f in set(bam_mappings.family):
        fam = bam_mappings[(bam_mappings.family==f) & (bam_mappings.relationship=='sibling')]
        affected_females = fam[(fam.sex_numeric=='2.0') & (fam.derived_affected_status=='autism')]
        affected_males = fam[(fam.sex_numeric=='1.0') & (fam.derived_affected_status=='autism')]
        unaffected_females = fam[(fam.sex_numeric=='2.0') & (pd.isna(fam.derived_affected_status))]
        unaffected_males = fam[(fam.sex_numeric=='1.0') & (pd.isna(fam.derived_affected_status))]

        male_pairs = male_pairs + [(i,j) for i in affected_males.index for j in unaffected_males.index if ((i in samples) and (j in samples))]
        female_pairs = female_pairs + [(i,j) for i in affected_females.index for j in unaffected_females.index if ((i in samples) and (j in samples))]
    affecteds = [a for a,u in (male_pairs + female_pairs)]
    unaffecteds = [u for a,u in (male_pairs + female_pairs)]    


    pvals = np.zeros(100000) + np.nan
    effect_size = np.zeros(100000) + np.nan
    sig_covs_vcf = pd.DataFrame()
    eps = 1e-20
    file = '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/counts/unmapped_filt.tsv'
    for covs in pd.read_table(file, chunksize=1000, nrows=len(pvals), skiprows=N_BATCH*len(pvals), header=None, index_col=None):
        print(covs.index[0])
        covs.drop(0, inplace=True, axis=1)
        covs.columns = list(bam_mappings.index)
        covs_norm = covs[abs(covs[affecteds].values-covs[unaffecteds].values).sum(axis=1)>0]
        pvals[covs_norm.index] = [stats.wilcoxon(q[1][affecteds]+eps, q[1][unaffecteds]+eps, zero_method='pratt', alternative='greater').pvalue for q in covs_norm.iterrows()]
        effect_size[covs_norm.index] = [sum(q[1][affecteds].values >= q[1][unaffecteds].values)/sum(q[1][unaffecteds].values >= q[1][affecteds].values) for q in covs_norm.iterrows()]
        sig_covs_vcf = pd.concat([sig_covs_vcf, covs_norm[(.5-abs(.5-pvals[covs_norm.index]))<(.05/10000000)]])

    # Set up dataframe to save.    
    pvals_asd = np.array([2*min(p, 1-p) for p in pvals])
    idx = np.array([i for i,p in enumerate(pvals_asd) if ~np.isnan(p)])
    effect_size_asd=np.array(effect_size)
    effect_size_asd = effect_size_asd[~np.isnan(pvals_asd)]
    pvals_asd = pvals_asd[~np.isnan(pvals_asd)]
    df = pd.DataFrame([pvals_asd, effect_size_asd], columns=idx).transpose()
    df.index = df.index + N_BATCH*len(pvals)
    df.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/pvals_asd/pvals_asd_%04d.tsv' % N_BATCH, sep='\t', header=None)
    sig_covs_vcf.index = sig_covs_vcf.index  + N_BATCH*len(pvals)
    sig_covs_vcf.to_csv('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/sig_covs_asd/sig_covs_asd_%04d.tsv' % N_BATCH, sep='\t', header=None)



