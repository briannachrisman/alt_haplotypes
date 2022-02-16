#!/bin/sh
#SBATCH --job-name=family_likelihoods_unmapped
#SBATCH --partition=owners
#SBATCH --array=1
#SBATCH --output=/scratch/users/briannac/logs/family_likelihoods_unmapped_%a.out
#SBATCH --error=/scratch/users/briannac/logs/family_likelihoods_unmapped_%a.err
#SBATCH --time=40:00:00
#SBATCH --mem=20G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu

## 875 families total -- 727 should actually work.

### file at /home/groups/dpwall/briannac/alt_haplotypes/src/localize/family_likelihoods_unmapped.sh

## Families possible are 1,10,100,102,104,105,106,107,108,11,110,111,112,113,114,115,116,117,118,119,12,120,121,123,124,125,126,127,128,129,13,130,131,132,133,134,135,136,137,138,139,14,140,141,142,143,144,145,146,147,148,149,15,150,151,152,153,154,156,157,158,159,16,160,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,178,179,18,180,181,182,183,184,185,186,188,189,19,190,191,192,193,194,196,197,198,199,2,20,201,202,203,204,205,206,207,208,209,21,210,211,212,213,214,215,216,217,218,219,22,220,221,222,223,224,225,229,23,230,231,234,235,236,237,238,24,241,242,243,244,246,247,248,249,25,250,251,252,253,254,255,257,258,259,26,260,261,262,264,265,266,267,268,269,27,270,271,272,273,274,276,277,278,279,28,280,281,282,283,284,285,286,288,289,29,290,291,292,293,294,295,296,297,298,299,3,30,300,301,302,304,305,306,307,308,31,311,313,314,315,316,317,318,32,320,321,323,324,327,329,33,330,331,332,333,335,336,337,338,339,34,340,341,342,343,344,345,346,347,348,349,35,350,351,352,353,354,355,356,358,359,36,360,361,362,363,364,365,366,367,368,369,37,370,371,372,373,374,375,376,377,379,38,380,381,382,383,385,387,388,389,39,390,391,392,393,394,395,396,397,398,399,4,40,402,403,404,405,406,407,408,409,41,410,411,412,414,415,416,417,418,419,42,420,421,422,425,426,427,428,429,43,430,431,434,435,436,437,438,439,44,440,442,443,444,445,446,447,448,449,45,450,451,452,454,455,456,457,458,46,460,461,462,463,464,465,466,467,468,469,47,471,472,473,474,476,477,478,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,498,499,50,500,501,502,503,504,505,509,51,510,511,512,514,515,516,517,518,519,52,520,521,522,523,524,525,528,529,530,531,532,533,534,535,536,537,538,539,54,540,541,542,543,544,545,548,549,55,550,551,552,553,554,555,556,557,558,559,56,560,561,562,563,564,565,566,567,568,569,57,570,571,572,574,575,576,577,578,579,58,580,581,583,584,585,586,587,588,590,591,594,595,596,597,598,599,60,600,601,602,603,604,605,606,607,608,609,61,610,611,612,613,614,615,616,617,618,619,62,620,621,622,623,624,625,627,629,63,632,633,634,637,638,639,64,640,641,642,643,644,645,646,647,648,649,65,650,652,653,654,656,657,658,659,66,660,661,662,663,664,665,667,668,669,67,670,671,672,673,674,675,676,678,679,68,680,681,682,683,684,685,686,687,688,689,69,690,691,692,694,695,698,699,7,70,700,702,703,704,705,706,707,708,709,71,710,712,713,714,715,716,717,718,719,72,720,721,722,723,725,726,727,729,73,730,732,736,737,738,739,74,740,741,742,743,744,745,746,747,748,749,75,751,752,753,754,755,757,758,759,76,760,761,762,763,764,765,766,767,768,77,770,772,773,774,776,777,778,779,78,781,782,783,784,786,787,788,789,79,790,791,792,793,794,796,797,798,799,8,80,801,803,805,806,81,812,813,814,815,818,819,82,821,823,825,827,828,83,836,839,84,840,842,85,852,853,854,855,857,86,860,862,863,867,869,87,870,88,89,9,90,91,94,96,97,98,99


cd $MY_HOME/alt_haplotypes
N=$((SLURM_ARRAY_TASK_ID-1))
N_digits=$(printf "%03d" $N)
N_KMERS=104565782 # Number of k-mers/counts present in file.



ml python/3.6.1

if [ ! -f intermediate_files/family_likelihoods/unmapped/likelihood_matrix_phasings_kmers_fam${N_digits}.tsv ]; then
        python3.6 -u src/localize/family_likelihoods.py $N intermediate_files/family_likelihoods/unmapped/ \
             intermediate_files/counts/unmapped_filt.tsv $N_KMERS
fi
