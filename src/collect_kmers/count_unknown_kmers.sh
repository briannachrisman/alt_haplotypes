#!/bin/sh
#SBATCH --job-name=count_unknown_kmers
#SBATCH --partition=owners
#SBATCH --array=1
#SBATCH --output=/scratch/users/briannac/logs/count_unknown_kmers_%a.out
#SBATCH --error=/scratch/users/briannac/logs/count_unknown_kmers_%a.err
#SBATCH --time=10:00:00
#SBATCH --mem=20G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briannac@stanford.edu


module load biology jellyfish bedtools samtools

# Note: Copy data file to intermediate file in $SCRATCH directory for faster xargs access.
# cp /home/groups/dpwall/briannac/alt_haplotypes/data/unknown_alt_haplotype_kmers.txt $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/unknown_alt_haplotype_kmers.txt


### file at /home/groups/dpwall/briannac/alt_haplotypes/src/unplaced_decoy_seqs/count_unknown_kmers.sh
unfinished_samples=$MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/unfinished.txt
cd $SCRATCH/tmp
for I_TO_ADD in 0 1000; do
    N=$((SLURM_ARRAY_TASK_ID + I_TO_ADD))
    head -n $N $unfinished_samples | tail -n 1 > $SCRATCH/tmp/tmp_kmers_from_unmapped_reads_$SLURM_ARRAY_TASK_ID.txt
    while read SAMPLE; do
        echo $SAMPLE
        mkdir $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/$SAMPLE
        cd $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/$SAMPLE
        
        echo "Making fastq from reads mapped to alt_haps..."
        for contig in chr1_KI270762v1_alt chr1_KI270766v1_alt chr1_KI270760v1_alt chr1_KI270765v1_alt chr1_GL383518v1_alt chr1_GL383519v1_alt chr1_GL383520v2_alt chr1_KI270764v1_alt chr1_KI270763v1_alt chr1_KI270759v1_alt chr1_KI270761v1_alt chr2_KI270770v1_alt chr2_KI270773v1_alt chr2_KI270774v1_alt chr2_KI270769v1_alt chr2_GL383521v1_alt chr2_KI270772v1_alt chr2_KI270775v1_alt chr2_KI270771v1_alt chr2_KI270768v1_alt chr2_GL582966v2_alt chr2_GL383522v1_alt chr2_KI270776v1_alt chr2_KI270767v1_alt chr3_JH636055v2_alt chr3_KI270783v1_alt chr3_KI270780v1_alt chr3_GL383526v1_alt chr3_KI270777v1_alt chr3_KI270778v1_alt chr3_KI270781v1_alt chr3_KI270779v1_alt chr3_KI270782v1_alt chr3_KI270784v1_alt chr4_KI270790v1_alt chr4_GL383528v1_alt chr4_KI270787v1_alt chr4_GL000257v2_alt chr4_KI270788v1_alt chr4_GL383527v1_alt chr4_KI270785v1_alt chr4_KI270789v1_alt chr4_KI270786v1_alt chr5_KI270793v1_alt chr5_KI270792v1_alt chr5_KI270791v1_alt chr5_GL383532v1_alt chr5_GL949742v1_alt chr5_KI270794v1_alt chr5_GL339449v2_alt chr5_GL383530v1_alt chr5_KI270796v1_alt chr5_GL383531v1_alt chr5_KI270795v1_alt chr6_GL000250v2_alt chr6_KI270800v1_alt chr6_KI270799v1_alt chr6_GL383533v1_alt chr6_KI270801v1_alt chr6_KI270802v1_alt chr6_KB021644v2_alt chr6_KI270797v1_alt chr6_KI270798v1_alt chr7_KI270804v1_alt chr7_KI270809v1_alt chr7_KI270806v1_alt chr7_GL383534v2_alt chr7_KI270803v1_alt chr7_KI270808v1_alt chr7_KI270807v1_alt chr7_KI270805v1_alt chr8_KI270818v1_alt chr8_KI270812v1_alt chr8_KI270811v1_alt chr8_KI270821v1_alt chr8_KI270813v1_alt chr8_KI270822v1_alt chr8_KI270814v1_alt chr8_KI270810v1_alt chr8_KI270819v1_alt chr8_KI270820v1_alt chr8_KI270817v1_alt chr8_KI270816v1_alt chr8_KI270815v1_alt chr9_GL383539v1_alt chr9_GL383540v1_alt chr9_GL383541v1_alt chr9_GL383542v1_alt chr9_KI270823v1_alt chr10_GL383545v1_alt chr10_KI270824v1_alt chr10_GL383546v1_alt chr10_KI270825v1_alt chr11_KI270832v1_alt chr11_KI270830v1_alt chr11_KI270831v1_alt chr11_KI270829v1_alt chr11_GL383547v1_alt chr11_JH159136v1_alt chr11_JH159137v1_alt chr11_KI270827v1_alt chr11_KI270826v1_alt chr12_GL877875v1_alt chr12_GL877876v1_alt chr12_KI270837v1_alt chr12_GL383549v1_alt chr12_KI270835v1_alt chr12_GL383550v2_alt chr12_GL383552v1_alt chr12_GL383553v2_alt chr12_KI270834v1_alt chr12_GL383551v1_alt chr12_KI270833v1_alt chr12_KI270836v1_alt chr13_KI270840v1_alt chr13_KI270839v1_alt chr13_KI270843v1_alt chr13_KI270841v1_alt chr13_KI270838v1_alt chr13_KI270842v1_alt chr14_KI270844v1_alt chr14_KI270847v1_alt chr14_KI270845v1_alt chr14_KI270846v1_alt chr15_KI270852v1_alt chr15_KI270851v1_alt chr15_KI270848v1_alt chr15_GL383554v1_alt chr15_KI270849v1_alt chr15_GL383555v2_alt chr15_KI270850v1_alt chr16_KI270854v1_alt chr16_KI270856v1_alt chr16_KI270855v1_alt chr16_KI270853v1_alt chr16_GL383556v1_alt chr16_GL383557v1_alt chr17_GL383563v3_alt chr17_KI270862v1_alt chr17_KI270861v1_alt chr17_KI270857v1_alt chr17_JH159146v1_alt chr17_JH159147v1_alt chr17_GL383564v2_alt chr17_GL000258v2_alt chr17_GL383565v1_alt chr17_KI270858v1_alt chr17_KI270859v1_alt chr17_GL383566v1_alt chr17_KI270860v1_alt chr18_KI270864v1_alt chr18_GL383567v1_alt chr18_GL383570v1_alt chr18_GL383571v1_alt chr18_GL383568v1_alt chr18_GL383569v1_alt chr18_GL383572v1_alt chr18_KI270863v1_alt chr19_KI270868v1_alt chr19_KI270865v1_alt chr19_GL383573v1_alt chr19_GL383575v2_alt chr19_GL383576v1_alt chr19_GL383574v1_alt chr19_KI270866v1_alt chr19_KI270867v1_alt chr19_GL949746v1_alt chr20_GL383577v2_alt chr20_KI270869v1_alt chr20_KI270871v1_alt chr20_KI270870v1_alt chr21_GL383578v2_alt chr21_KI270874v1_alt chr21_KI270873v1_alt chr21_GL383579v2_alt chr21_GL383580v2_alt chr21_GL383581v2_alt chr21_KI270872v1_alt chr22_KI270875v1_alt chr22_KI270878v1_alt chr22_KI270879v1_alt chr22_KI270876v1_alt chr22_KI270877v1_alt chr22_GL383583v2_alt chr22_GL383582v2_alt chrX_KI270880v1_alt chrX_KI270881v1_alt chr19_KI270882v1_alt chr19_KI270883v1_alt chr19_KI270884v1_alt chr19_KI270885v1_alt chr19_KI270886v1_alt chr19_KI270887v1_alt chr19_KI270888v1_alt chr19_KI270889v1_alt chr19_KI270890v1_alt chr19_KI270891v1_alt chr1_KI270892v1_alt chr2_KI270894v1_alt chr2_KI270893v1_alt chr3_KI270895v1_alt chr4_KI270896v1_alt chr5_KI270897v1_alt chr5_KI270898v1_alt chr6_GL000251v2_alt chr7_KI270899v1_alt chr8_KI270901v1_alt chr8_KI270900v1_alt chr11_KI270902v1_alt chr11_KI270903v1_alt chr12_KI270904v1_alt chr15_KI270906v1_alt chr15_KI270905v1_alt chr17_KI270907v1_alt chr17_KI270910v1_alt chr17_KI270909v1_alt chr17_JH159148v1_alt chr17_KI270908v1_alt chr18_KI270912v1_alt chr18_KI270911v1_alt chr19_GL949747v2_alt chr22_KB663609v1_alt chrX_KI270913v1_alt chr19_KI270914v1_alt chr19_KI270915v1_alt chr19_KI270916v1_alt chr19_KI270917v1_alt chr19_KI270918v1_alt chr19_KI270919v1_alt chr19_KI270920v1_alt chr19_KI270921v1_alt chr19_KI270922v1_alt chr19_KI270923v1_alt chr3_KI270924v1_alt chr4_KI270925v1_alt chr6_GL000252v2_alt chr8_KI270926v1_alt chr11_KI270927v1_alt chr19_GL949748v2_alt chr22_KI270928v1_alt chr19_KI270929v1_alt chr19_KI270930v1_alt chr19_KI270931v1_alt chr19_KI270932v1_alt chr19_KI270933v1_alt chr19_GL000209v2_alt chr3_KI270934v1_alt chr6_GL000253v2_alt chr19_GL949749v2_alt chr3_KI270935v1_alt chr6_GL000254v2_alt chr19_GL949750v2_alt chr3_KI270936v1_alt chr6_GL000255v2_alt chr19_GL949751v2_alt chr3_KI270937v1_alt chr6_GL000256v2_alt chr19_GL949752v1_alt chr6_KI270758v1_alt chr19_GL949753v2_alt chr19_KI270938v1_alt; do

            
            # Create fastq file with reads mapping to any alternative haplotypes.
            samtools view -F 0x100 -F 0x400 -q 60 -F 0x200 s3://ihart-hg38/cram/$SAMPLE.final.cram $contig -b | bedtools bamtofastq -i - -fq kmers.${contig}.fastq
        done
    \rm *.crai
    

    # Count all kmers from alt haplotype fastqs.
    echo "Counting all kmers..."
    jellyfish count --canonical -m 100 -s 100M -L 2  -o kmers.jf kmers.*.fastq
    \rm kmers.*.fastq
    
    # Query specific "unlocalized" alternative haplotype kmers./home/groups/dpwall/briannac/alt_haplotypes/data/unknown_alt_haplotype_kmers.txt
    echo "Querying specific unknown alt hap kmers..."
    cut -f1 $MY_HOME/alt_haplotypes/intermediate_files/unplaced_decoy_seqs/sample_kmer_counts/unknown_alt_haplotype_kmers.txt | xargs jellyfish query kmers.jf | awk  '{print $2}' > kmer_counts.txt
    \rm kmers.jf
    
    echo "Splitting files..."
    split -l 100000 -d -a 3 --additional-suffix=.txt kmer_counts.txt kmer_counts. # Split into many 100K line files.

    \rm kmer_counts.txt
    
    done < $SCRATCH/tmp/tmp_kmers_from_unmapped_reads_$SLURM_ARRAY_TASK_ID.txt
    \rm $SCRATCH/tmp/tmp_kmers_from_unmapped_reads_$SLURM_ARRAY_TASK_ID.txt 
done



