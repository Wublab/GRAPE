#mutation selection
import argparse
import os
import math
import time


def get_parser():
    parser = argparse.ArgumentParser(description='GRAPE copy files')
    #parser.parse_args()
    parser.add_argument("-o", "--outdir", help="output directory")
    parser.add_argument("-p", "--pdbdir", help="directory of pdb files, ie. /home/user/GRAPE/foldx/")
    parser.add_argument("-l", '--listfile',help='list file of energies, varied from software')
    parser.add_argument("-s", "--software", help="software name")
    parser.add_argument("-c", '--cutoff', help='ddg cutoff')
    parser.add_argument("-sf", '--filesuffix', help='file suffix, ie. 5XJH_protein_Repair.pdb')
    #args = parser.parse_args()
    return parser


def foldxfilter(foldxout,ddgcutoff):
    ddg_dict = {}
    foldxoutfile = open(foldxout)
    foldxselectlist = []
    for line in foldxoutfile:
        lst = line.split("\t")
        name = lst[0].split("_")[0]
        number = lst[0].split("_")[1]
        dg = float(lst[1])
        try:
        #if number in ddg_dict:
            ref_dg = ddg_dict[number]["ref"]
            ddg = dg - ref_dg
            if ddg < ddgcutoff:
                ddg_dict[number][name] = ddg
        except KeyError:
            ddg_dict[number] = {}
            ddg_dict[number]["ref"] = dg
    for pos in ddg_dict:
        for res in ddg_dict[pos]:
            if res != "ref":
                foldxselectlist.append(pos+"_"+res+"\t"+str(ddg_dict[pos][res]))
                #print(pos+"_"+res+"\t"+str(ddg_dict[pos][res]))
    return foldxselectlist


import os
def copyfiles(filesuffix,pdbdir,targetdir,selectedlist):
    namedlist = []
    for x in selectedlist:
        #print(x)
        number = x.split("\t")[0].split("_")[0]
        mt = x.split("\t")[0].split("_")[1]
        prefix = mt+number+"_"
        name = prefix+filesuffix
        namedlist.append(name)
        os.system("cp "+pdbdir+name+" "+targetdir)

def _1_2_3(oneletteraa):
    aadict = {'C':"CYS", 'D':"ASP", 'S':"SER", 'N':"ASN", 'K':"LYS",
              'I':"ILE", 'P':"PRO", 'T':"THR", 'F':"PHE", 'Q':"GLN",
              'G':"GLY", 'H':"HIS", 'L':"LEU", 'R':"ARG", 'W':"TRP",
              'A':"ALA", 'V':"VAL", 'E':"GLU", 'Y':"TYR", 'M':"MET"}
    return aadict[oneletteraa]
        
def rosettafilter(rosettaout,ddgcutoff):
    rosetta_ddg_file = open(rosettaout)
    rosettaselectlist = []
    for line in rosetta_ddg_file:
        #print(line)
        try:
            lst = line.split(":")[1].split()
            mutation = lst[0]
            if mutation != "description":
                number = mutation[1:-1]
                mt = _1_2_3(mutation[-1])
                ddg = float(lst[1])
                if ddg < ddgcutoff:
                    rosettaselectlist.append(number+"_"+mt+"\t"+str(ddg))
        except IndexError:
            #print(line)
            continue
    return rosettaselectlist

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    
    outdir = args.outdir
    pdbdir = args.pdbdir
    listfile = args.listfile
    software = args.software
    cutoff = args.cutoff
    filesuffix = args.filesuffix
    
    if software == "foldx":
        foldxout = listfile
        foldxddgcutoff = cutoff
        selectedlist = foldxfilter(foldxout,foldxddgcutoff)
        targetdir = outdir
        copyfiles(filesuffix,pdbdir,targetdir,selectedlist)
        
    if software == "rosetta":
        rosettaout = listfile
        rosettaddgcutoff = cutoff
        selectedlist = rosettafilter(rosettaout,rosettaddgcutoff)
        targetdir = outdir
        copyfiles(filesuffix,pdbdir,targetdir,selectedlist)
        
    #if software == "ABACUS":
    if software not in ["foldx","rosetta","ABACUS"]:
        print("Unknown software!")
