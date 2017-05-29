import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input file to SRA run table.')
    parser.add_argument('-c', help='column with sample IDs', default='Sample_Name_s')
    parser.add_argument('-o', help='output file name')

    args = parser.parse_args()


    df = pd.read_csv(args.i, sep='\t')
    df = df[ [args.c] + [i for i in df.columns if i != args.c] ]

    df.to_csv(args.o, sep='\t', index=False)
