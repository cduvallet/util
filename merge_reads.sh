#!/bin/bash

# Merges fwd and rev fastqs in current director
# Puts merged fastq's in merged_fastqs/
# Puts merge logs in merge_logs/

for f in *_1.fastq
do
    usearch8 -fastq_mergepairs $f -reverse ${f%_1.fastq}_2.fastq \
        -fastqout ../merged_fastqs/${f%_1.fastq}.merged.fastq \
	-log ../merge_logs/${f%_1.fastq}.log 
done
