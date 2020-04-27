import argparse
import os

def get_parser():
    parser = argparse.ArgumentParser(description='parallel rosetta ddg scan')
    #parser.parse_args()
    parser.add_argument("-s", "--structure", help="your pdb file")
    parser.add_argument("-nt", "--number_threads", help="number of threads")
    #args = parser.parse_args()
    return parser

def gen_seq(pdb):
    seq = ''
    longer_names={'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
                  'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
                  'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
                  'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
                  'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}
    pdb = open(pdb)
    for line in pdb:
        if line.startswith("ATOM") and "CA" in line.split():
            amino_acid = line[17:20]
            seq = seq + longer_names[amino_acid]
        if line[0:3] == "TER":
            seq =seq + "\n"
    return seq

def gen_mutfile(seq):
    n = 0
    x = 0
    c = 0
    out = []
    #line.strip()
    for aa in seq.strip():
        n = n + 1
        for X in ['C', 'D', 'S', 'N', 'K','I', 'P', 'T', 'F', 'Q','G', 'H', 'L', 'R', 'W','A', 'V', 'E', 'Y', 'M']:
            if aa != X:
                x = x + 1
                c = c + 1
                out.append('1\n'+aa+" "+str(n)+" "+X)
    return out

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def split_mutfile(all_mutfile,nt):
    chunk_mutfile = chunkIt(all_mutfile,nt)
    n = 0
    for x in chunk_mutfile:
        n = n + 1
        of_name = "mtfile_"+str(n)
        of = open(of_name,"w+")
        of = open(of_name,"a+")
        print("total"+str(len(x)),file=of)
        for m in x:
            print(m,file=of)
            

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    pdb = args.structure
    nt = args.number_threads
    seq = gen_seq(pdb)
    all_mutfile = gen_mutfile(seq)
    split_mutfile(all_mutfile,nt)
