import sys
import re

def read_csv(file):
    """
    Function to read the csv, separating
    individuals' names and genotypic data.
    """
    with open(file, "r") as f:
        dat = f.read().splitlines()
    dat = [ re.sub(" +","",x).split(",") for x in dat ]
    indiv = [ x[0] for x in dat ]
    markers = [ [ int(j) for j in x[1:] ] for x in dat ]
    return(indiv, markers)

def find_best_motif(locus):
    """
    Looks for the optimal motif size,
    checking for the size (2-10) that has highest
    average of exact divisions. Exact divisions are
    calculated on the difference in length between
    an allele_i and the shortest allele for that locus:

    (A_i - A_min) % m [ i .. n ]

    If multiple motifs are equally good, the longest one is favored.
    """
    motif = range(2,11)
    mprop = []
    for m in motif:
        y = [ (x - min(locus)) % m for x in locus if x != 0 ]
        mprop.append(round(float(sum([ x == 0 for x in y ]))/len(y),2)) # get the proportion with exact divisions
    shortest = min([ x for x in locus if x != 0 ]) # get shortest allele
    bprop = max(mprop)
    besti = [ i for i in range(len(mprop)) if mprop[i] == bprop ]
    bestm = max([ motif[i] for i in besti])
    return(bestm,shortest,mprop)

def get_motif(markers):
    """
    Find the best motif and the shortest allele for each locus.
    Returns a two lists with each.
    """
    markerstr = list(zip(*markers)) # transpose matrix
    motif = []
    shortest = []
    cols = len(markerstr)
    for i in range(1,cols,2): # loop for each column
        locus = markerstr[i-1]+markerstr[i] # merge both alleles
        best,short,_ = find_best_motif(locus)
        motif.append(best)
        shortest.append(short)
    return(motif,shortest)

def get_repeats(markers, motif, shortest):
    """
    Converts genotypic length data into repeats.
    Diploid data is spliced into two matrices (a,b).
    """
    repeats_a = []
    repeats_b = []
    for marker in markers:
        cols = len(marker)
        r_a = []
        r_b = []
        for i in range(1,cols,2):
            if sys.version_info[0] >= 3:
                ii = int(i - (i/2) - 1/2) # use i to generate an index from 0 .. n-1
            else:
                ii = int(i - (i/2) - 1/2) - 1
            if marker[i-1] == 0:
                r_a.append("?")
            else:
                r = ((marker[i-1] - shortest[ii]) / motif[ii]) + 1
                r_a.append(int(round(r)))
            if marker[i] == 0:
                r_b.append("?")
            else:
                r = ((marker[i] - shortest[ii]) / motif[ii]) + 1
                r_b.append(int(round(r)))
        repeats_a.append(r_a)
        repeats_b.append(r_b)
    return(repeats_a, repeats_b)

def to_csv(repeats_a, repeats_b, indiv):
    """
    CSV output function. Generates two files; one
    for each allele (ouput_a.csv, output_b.csv).
    """
    with open("output_a.csv", "w") as A, open("output_b.csv", "w") as B:
        for i in range(len(indiv)):
            row = ",".join([indiv[i]]+[ str(x) for x in repeats_a[i] ]) + "\n"
            A.write(row)
            row = ",".join([indiv[i]]+[ str(x) for x in repeats_b[i] ]) + "\n"
            B.write(row)

if __name__ == "__main__":
    file = sys.argv[1]
    indiv, markers = read_csv(file)
    motif,shortest = get_motif(markers)
    repeats_a, repeats_b = get_repeats(markers, motif, shortest)
    to_csv(repeats_a, repeats_b, indiv)

# flatten = [item for sublist in list(zip(repeats_a[3], repeats_b[3])) for item in sublist]
