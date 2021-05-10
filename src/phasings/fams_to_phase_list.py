import glob
FAM_OUT_FILE = '/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/phasings/fams_to_phase.csv'
fams = [f.split('/')[-1].replace('.phased.txt', '') for f in glob.glob('/oak/stanford/groups/dpwall/users/kpaskov/PhasingFamilies/phased_ihart.ms2_del/*.phased.txt')]
with open(FAM_OUT_FILE, 'w') as file:
    for i,f in enumerate(fams):
        file.write( f + '\n')