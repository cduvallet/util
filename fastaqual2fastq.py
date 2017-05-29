"""
Combines separate fasta and quality files to a fastq file.

Assumes fasta and quality files have corresponding lines.

Quality scores should be space-delimited numbers.

Quality score dictionary built from http://drive5.com/usearch/manual/quality_score.html
"""
import util
import argparse

def qual2code(encoding='33'):
    if encoding == '33':
        s = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK"
        d = {str(i): j for i, j in zip(range(0, 43), s)}
    return d

def parse_files(f, q):
    """
    Parse fasta and quality files, f and q
    """
    sids = []
    seqs = []
    quals = []

    for sid, seq in util.iter_fst(f):
        sids.append(sid[1:])
        seqs.append(seq)

    for _, qual in util.iter_fst(q):
        quals.append(qual.split(' '))

    if len(sids) != len(seqs) != len(quals):
        raise ValueError('fasta and quality files are not the same length!')

    return sids, seqs, quals

def parse_quals(quals, encoding):
    """
    quals is a list of lists containing quality scores (numbers)
    """
    d = qual2code(encoding)
    print(d)
    newquals = []
    for qual in quals:
        newquals.append([d[q] for q in qual])
    return newquals

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fasta', help='input fasta file')
    parser.add_argument('quality', help='corresponding quality file')
    parser.add_argument('out', help='output fastq file name')
    parser.add_argument('-e', help='ascii encoding for output fastq. currently only supports 33', \
                        default='33', type=str)
    args = parser.parse_args()
    seqIDs, seqs, quals = parse_files(args.fasta, args.quality)
    print(len(seqIDs), len(seqs), len(quals), len(quals[0]))

    quals = parse_quals(quals, encoding=args.e)

    with open(args.out, 'w') as f:
        for i in range(len(seqIDs)):
            if len(seqs[i]) == len(quals[i]):
                f.write('@' + seqIDs[i] + '\n' + seqs[i] + \
                        '\n+\n' + ''.join(quals[i]) + '\n')
            else:
                raise ValueError('mismatched sequence and quality score lengths')
