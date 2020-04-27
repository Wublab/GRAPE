#mutation selection
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
def copyfiles(filesuffix,targetdir,selectedlist):
    namedlist = []
    for x in selectedlist:
        #print(x)
        number = x.split("\t")[0].split("_")[0]
        mt = x.split("\t")[0].split("_")[1]
        prefix = mt+number+"_"
        name = prefix+filesuffix
        namedlist.append(name)
        os.system("cp "+name+" "+targetdir)

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

foldxout = "/home/jsun/GRAPE/foldx/energies_all.txt"
rosettaout = "/home/jsun/GRAPE/rosetta/test/ddg_predictions.out"
foldxddgcutoff = -2
rosettaddgcutoff = -5
foldxlist = foldxfilter(foldxout,foldxddgcutoff)
rosettalist = rosettafilter(rosettaout,rosettaddgcutoff)
filesuffix="5XJH_protein_Repair.pdb"
targetdir = "/home/jsun/GRAPE/selectedpdbs/"
selectedlist = foldxlist+rosettalist
copyfiles(filesuffix,targetdir,selectedlist)
