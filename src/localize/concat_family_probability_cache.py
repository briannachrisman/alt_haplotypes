import pickle
import time

family_probability_dict = {}
for N_PHASE in range(250):
    t = time.time()
    with open('/home/groups/dpwall/briannac/alt_haplotypes/intermediate_files/localize/family_probability_cache_%i.pickle' % N_PHASE, 'rb') as f:
        family_probability_dict = {**family_probability_dict, **(pickle.load(f))}
    print(time.time()-t, N_PHASE)

with open('/home/groups/dpwall/briannac/alt_haplotypes/data/localize/family_probability_cache.pickle', 'wb') as f:
    pickle.dump(family_probability_dict, f, protocol=pickle.HIGHEST_PROTOCOL)