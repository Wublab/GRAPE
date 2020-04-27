seq = open("/home/jsun/atta/rosetta/ddg/protein_0002_0164.pdb.fasta")
for line in seq:
    if not line.startswith(">"):
        n = 0
        x = 0
        c = 0
        out = ""
        #line.strip()
        for aa in line.strip():
            n = n + 1
            for X in ['C', 'D', 'S', 'N', 'K','I', 'P', 'T', 'F', 'Q','G', 'H', 'L', 'R', 'W','A', 'V', 'E', 'Y', 'M']:
                if aa != X:
                    x = x + 1
                    c = c + 1
                    out = out + '1\n'+aa+" "+str(n)+" "+X+"\n"
print("total "+str(c)+"\n"+out)
