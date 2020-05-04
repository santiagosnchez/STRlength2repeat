# STRlength2repeat

This program is meant to convert Short Tandem Repeat (STR) length data to number of tandem repetitions. This is specially useful for applying models of microsatellite evolution (Sainudiin et al. 2004)[#references] to infer divergence times or demographic models.

The CSV output can be uploaded directly to [BEAST v2.6.2](https://github.com/CompEvol/beast2/releases) by installing the [BEASTvntr](https://github.com/rbouckaert/BEASTvntr) package.

## Dependencies

Code is written to be functional under Python 2 and 3. However, I suggest using Python 3 to avoid future issues. Other than that, there are no other dependencies.

## Installation

```
wget https://raw.githubusercontent.com/santiagosnchez/STRlength2repeat/master/STRlength2repeat.py
```

## Running the code

```
python3 STRlength2repeat.py input_file.csv
```

## Input file

The program expects a CSV file with STR data in standard length format.
For example:

```
indiv1,124,124,345,347,233,239
indiv2,122,124,345,345,230,239
...
```

# References

Sainudiin R, Durrett RT, Aquadro CF, Nielsen R. Microsatellite mutation models: insights from a comparison of humans and chimpanzees. Genetics. 2004;168(1):383‐395. doi:10.1534/genetics.103.022665
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1448085/
