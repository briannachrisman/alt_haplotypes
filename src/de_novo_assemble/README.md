# De Novo Assemble

De novo assembling contigs made from unmapped reads.

## Pre-requisites
Collect_kmers, localize.

## Storage

## Pipeline

1.   ```compute_cluster.sh```: Computes clusters of k-mers based on start/stop locations.
    - ***Inputs***: ``../blood_microbiome/intermediate_files/kraken_align/<SAMPLE>.unclassified.fastq```
    - ***Outputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.unmapped.jf```, ```../intermediate_files/kmers/<SAMPLE>.jellyfish.unmapped.fa```

2.  ```bin_kmers.sh```: Bins k-mers into bins.
    - ***Inputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.kmers.unmapped_reads.fa```
    - ***Outputs***: ```../intermediate_files/kmers/kmers.unmapped_reads.list```

3.  ```de_novo_assemble.sh```: Compute list of non-unique k-mers. Note: 264,492,894 total shared kmers.
    - ***Inputs***: ```../intermediate_files/kmers/<SAMPLE>/<SAMPLE>.jellyfish.kmers.unmapped_reads.fa```
    - ***Outputs***: ```../intermediate_files/kmers/kmers.unmapped_reads.list```
