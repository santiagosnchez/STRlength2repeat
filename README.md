# STRlength2repeat

This program is meant to convert Short Tandem Repeat (STR) length data to number of tandem repetitions. This is specially useful for applying models of microsatellite evolution \([Sainudiin et al. 2004](#references)\) to infer divergence times or demographic models.

The CSV output can be uploaded directly to [BEAST v2.6.2](https://github.com/CompEvol/beast2/releases) by installing the [BEASTvntr](https://github.com/rbouckaert/BEASTvntr) package.

## Dependencies

Code is written to be functional under Python 2 and 3. However, I suggest using Python 3 to avoid future issues. Other than that, there are no other dependencies.

## Installation

```bash
wget https://raw.githubusercontent.com/santiagosnchez/STRlength2repeat/master/STRlength2repeat.py
```

## Running the code

```bash
python3 STRlength2repeat.py input_file.csv
```

## Input file

The program expects a CSV file with STR data in standard length format.
For example:

```bash
indiv1,124,124,345,347,233,239
indiv2,122,124,345,345,230,239
...
```

Here, both alleles for a single locus are contiguous. This means that if there are `n` STR loci then there will be `(n * 2) + 1` columns.

## Tandem size

The program includes a function to infer the the size of the tandem, which is based on the difference between minimum allele `(A_i - A_min) % m`, where `m` is the size of the tandem. In this case, `m` can go from 2 to 10.

```python
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
```

A predefined tandem size should be easy to implement by providing it in CSV format. That will be done in future versions.

## Function for repeat number

The repeat number function is wrapped around `get_repeats()` and follows this logic: for `i` alleles `A` within locus `j` we take the difference between the `A_ij` and the minimum/shortest allele `A_minj` and divide it by the tandem size `m` and adding 1:

`(A_ij - A_minj) / m_j) + 1`

# References

Sainudiin R, Durrett RT, Aquadro CF, Nielsen R. Microsatellite mutation models: insights from a comparison of humans and chimpanzees. Genetics. 2004;168(1):383‐395. doi:10.1534/genetics.103.022665
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1448085/
