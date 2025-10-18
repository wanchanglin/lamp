# LAMP - Liverpool Annotation of metabolites using Mass sPectrometry

## Introduction

Untargeted metabolomics studies routinely apply liquid chromatography-mass
spectrometry to acquire data for hundreds or low thousands of metabolites
and exposome-related (bio)chemicals. The annotation or higher-confidence
identification of metabolites and biochemicals can apply multiple different
data types (1) chromatographic retention time, (2) the mass-to-charge
(*m/z*) ratio of ions formed during electrospray ionisation for the
structurally intact metabolite or (bio)chemical and (3) fragmentation mass
spectra derived from MS/MS or MS^n^ experiments.

Commonly, the mass-to-charge (*m/z*) ratio of ions formed during
electrospray ionisation for the structurally intact metabolite are applied
as a first step in the annotation process. Importantly, a single metabolite
can be detected as multiple different ion types (adducts, isotopes,
in-source fragments, oligomers) and grouping together of features
representing the same metabolite or biochemical can decrease the number of
false positive annotations. The Liverpool Annotation of metabolites using
Mass sPectrometry (LAMP) is a Python package and an easy-to-use software for
feature grouping and metabolite annotation using MS1 data only. LAMP groups
features based on chromatographic retention time similarity and positive
response-based correlations across multiple biological samples. Genome-scale
metabolic models are the source of metabolites applied in the standard
reference files though any source of metabolites can be used (e.g. HMDB or
LIPIDMAPS). The *m/z* differences related to in-source fragments, adducts,
isotopes, oligomers and charge states can be user-defined in the reference
file.

## Installation

### PyPI

To install from [PyPI](https://pypi.org/) via `pip`, use the distribution
name `lamps`:

```bash
pip install lamps
```

This is the preferred installation method.

### Conda

`LAMP` is in `Bioconda` channel and use the following to install for conda:

```bash
conda install -c bioconda lamps
```

### Source

Install directly from GitHub: 

```bash
pip install git+https://github.com/wanchanglin/lamp.git
```

Update directly from GitHub branch `dev`:

```bash
pip install git+https://github.com/wanchanglin/lamp.git@dev --upgrade --no-deps --force-reinstall
```

## Usages

For end users, `LAMP` provides command line and graphical user interfaces.

    $ lamp --help
    Executing lamp version 1.0.4.
    usage: lamp [-h] {cli,gui} ...

    Compounds Annotation of LC-MS data

    positional arguments:
      {cli,gui}
        cli       Annotate metabolites in CLI.
        gui       Annotate metabolites in GUI.

    options:
      -h, --help  show this help message and exit

### Command line interface (CLI)

Use the follow command line to launch CLI mode: :

    $ lamp cli <arg_lists>

Here is an example: :

    lamp cmd \
      --sep "tab" \
      --input-data "./data/df_pos_3.tsv" \
      --col-idx "1, 2, 3, 4" \
      --add-path "" \
      --ref-path "" \
      --ion-mode "pos" \
      --cal-mass \
      --thres-rt "1.0" \
      --thres-corr "0.5" \
      --thres-pval "0.05" \
      --method "pearson" \
      --positive \
      --ppm "5.0" \
      --save-db \
      --save-mr \
      --db-out "./res/test.db" \
      --sr-out "./res/test_s.tsv" \
      --mr-out "./res/test_m.tsv"

### Graphical user interface (GUI)

    $ lamp gui

## Links

- Documentation: [Read the Docs](https://lamp-liverpool-annotation-of-metabolite-using-mass-spectrometry.readthedocs.io/en/latest/)
- PyPI: https://pypi.org/project/lamps/
- Bioconda: https://anaconda.org/bioconda/lamps
- DOI: [10.5281/zenodo.14711459](https://doi.org/10.5281/zenodo.14711458)

## Authors

- Wanchang Lin (<Wanchang.Lin@liverpool.ac.uk>), The University of Liverpool
- Warwick Dunn (<Warwick.Dunn@liverpool.ac.uk>), The University of Liverpool
