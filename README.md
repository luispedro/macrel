# Macrel: (Meta)genomic AMP Classification and Retrieval

Pipeline to mine antimicrobial peptides (AMPs) from (meta)genomes.

[![Build Status](https://github.com/BigDataBiology/macrel/workflows/Build%20Status/badge.svg)](https://github.com/BigDataBiology/macrel/workflows/Build%20Status/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/macrel/badge/?version=latest)](https://macrel.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Install with Bioconda](https://anaconda.org/bioconda/macrel/badges/downloads.svg)](https://anaconda.org/bioconda/macrel)
[![Install with Bioconda](https://anaconda.org/bioconda/macrel/badges/version.svg)](https://anaconda.org/bioconda/macrel)

If you use this software in a publication please cite

>   Santos-Júnior CD, Pan S, Zhao X, Coelho LP. 2020.
>   Macrel: antimicrobial peptide screening in genomes and metagenomes.
>   PeerJ 8:e10555. DOI: [10.7717/peerj.10555](https://doi.org/10.7717/peerj.10555)

Run Macrel online: [https://big-data-biology.org/software/macrel](https://big-data-biology.org/software/macrel)

## License

MIT.

Macrel as a whole is under the **MIT** license.

## Install

The recommended method of installation is through
[bioconda](https://anaconda.org/bioconda/macrel):

```bash
conda create --name env_macrel -c bioconda macrel
conda activate env_macrel
macrel -h
```

Alternatively, just:

```bash
conda install -c bioconda macrel
```

To install from source, [read the docs](https://macrel.readthedocs.io/en/latest/install)

### Examples

> Macrel uses a _subcommand interface_. You run `macrel COMMAND ...` with the
> COMMAND specifying which components of the pipeline you want to use.

To run these examples, first download the example sequences from
[github](https://github.com/BigDataBiology/macrel/tree/main/example_seqs), or
by running:

```bash
macrel get-examples
```

The main output file generated by Macrel consists of a table with 6 columns containing
the: sequence access code, peptide sequence, classification of peptide accordingly
composition and structure, the probability associated with the AMP prediction,
hemolytic activity prediction and probability associated to hemolytic activity
prediction. All peptides outputted in this table are considered AMPs (p > 0.5),
although peptides predicted as AMPs with probabilities closer to 1 are more likely
to be active. 

To run Macrel on peptides, use the `peptides` subcommand:

```bash
macrel peptides \
    --fasta example_seqs/expep.faa.gz \
    --output out_peptides
```

In this case, we use `example_seqs/expep.faa.gz` as the input sequence. This should
be an amino-acid FASTA file. The outputs will be written into a folder called
`out_peptides`, and Macrel will 4 threads. An example of output using
this mode can be found at `test/peptides/expected.prediction`.

To run Macrel on contigs, use the `contigs` subcommand:

```bash
macrel contigs \
    --fasta example_seqs/excontigs.fna.gz \
    --output out_contigs
```

In this example, we use the example file `excontigs.fna.gz` which is a FASTA
file with nucleotide sequences, writing the output to `out_contigs`.
An example of output using this mode can be found at `test/contigs/expected.prediction`.
Additionally to the prediction table, this mode also produces two files containing
general gene prediction information in the contigs and a fasta file containing the
predicted and filtered small genes (≤ 100 amino acids).

To run Macrel on paired-end reads, use the `reads` subcommand:

```bash
macrel reads \
    -1 example_seqs/R1.fq.gz \
    -2 example_seqs/R2.fq.gz \
    --output out_metag \
    --outtag example_metag
```

The paired-end reads are given as paired files (here, `example_seqs/R1.fq.gz`
and `example_seqs/R2.fq.gz`). If you only have single-end reads, you can omit
the `-2` argument. An example of outputs using this mode can be found at
`test/reads/expected.prediction` and `test/reads/expected.smorfs.faa`.
Additionally to the prediction table, this mode also produces a contigs fasta file, 
and the two files containing general gene prediction coordinates and a fasta file
containing the predicted and filtered small genes (≤ 100 amino acids).

To run Macrel to get abundance profiles, you only need the short reads file
and a reference with peptide sequences. Use the `abundance` subcommand:


```bash
macrel abundance \
    -1 example_seqs/R1.fq.gz \
    --fasta example_seqs/ref.faa.gz \
    --output out_abundance \
    --outtag example_abundance
```

This mode returns a table of abundances containing two columns, the first with the
name of the AMPs and the second with the number of reads mapped back to each peptide
using the given reference. An example of this output using the example file can be found
at `test/abundances/expected.abundance.txt`.

### AMPSphere Querying

Macrel also supports querying the [AMPSphere
database](https://ampsphere.big-data-biology.org/) (described in [Santos-Júnior
et al., 2024](https://doi.org/10.1016/j.cell.2024.05.013)). To do so, use the
`query-ampsphere` subcommand:

```bash
macrel query-ampsphere \
    --fasta example_seqs/pep8.faa \
    --output out_ampsphere
```

Note that, by default, this command requires internet access as it uses the
AMPSphere API. Alternatively, you can use the `--local` flag to download a copy
of the database and run the queries locally. This only requires the network the
first time.

```bash
macrel query-ampsphere \
    --local \
    --fasta example_seqs/pep8.faa \
    --output out_ampsphere
```

By default it performs exact matching, but you can also use MMSeqs2 to perform
approximate matching by using the `--query-mode=mmseqs` (or `--query-mode=hmm`
for HMMER).

### Community

Macrel is actively maintained to fix all issues and assimilate suggestions we
get from users (see [our commitments to high-quality
software](https://www.big-data-biology.org/software/commitments/)).

For general questions about macrel, we ask that you use the
[**AMPSphere Google Group (mailing list)**](https://groups.google.com/g/ampsphere-users).

Technical issues can be reported using [Github
issues](https://github.com/BigDataBiology/macrel/issues/).

