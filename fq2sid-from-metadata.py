
import pandas as pd
import argparse

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', help='input metadata/SRA table. assumes sample IDs are in first column')
    parse.add_argument('-r', help='column with SRR labels (should not have .fastq suffix', default='Run_s')
    parse.add_argument('-o', help='output fq2sid file', default='fq2sid.txt')
    parse.add_argument('-s', help='suffix to add to SRR labels', default='.fastq')
    args = parse.parse_args()

    df = pd.read_csv(args.i, sep='\t', index_col=0)
    with open(args.o, 'w') as f:
        for s, r in zip(df.index, df[args.r]):
            f.write(r + args.s + '\t' + s + '\n')
    
    
