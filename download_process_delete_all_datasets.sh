#!/usr/bin/env bash

# For each dataset in S3_to_process.txt,
# 1. download the data from S3
# 2. Run Master.py on the data
# 3. delete the data

while read f;
do
    aws s3 cp s3://mbit.storage.bucket1/${f} tmp_data/ --recursive
    python ~/scripts/Master.py -i ~/users/duvallet/data/reprocessing_all/tmp_data/
    # Remove the ~/proc folder
    d=$(cut tmp_data/summary_file.txt -f 2 | head -n 1)
    rm -r ~/proc/${d}_proc_16S
    # Remove the data
    rm -r tmp_data/*
done < S3_to_process.txt
