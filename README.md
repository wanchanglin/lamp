# LAMP - Liverpool Annotation of metabolites using Mass sPectrometry

## Introduction

The annotation or identification of metabolites detected in untargeted
metabolomics studies applying liquid chromatography-mass spectrometry can
apply full-scan (MS1), retention time (RT) and gas-phase fragmentation
(MS/MS) data. Full-scan MS1 data can be applied as a first pass to decrease
the number of possible annotations. However, electrospray ionisation is a
complex process which generates multiple features (m/z-RT pairs) for each
metabolite. The grouping of features and subsequent linkage to a single or
multiple molecular formula is required to maximise true positive annotations
and minimise false positive annotations.

LAMP is a Python package as an easy-to-use software for feature grouping and
metabolite annotation using MS1 data only. LAMPS groups features based on RT
similarity and positive correlations across multiple biological samples.
Genome-scale metabolic models are the source of metabolites applied in
reference files though any source of metabolites can be used (e.g. HMDB or
LIPID MAPS). The m/z differences related to in-source fragments, adducts,
isotopes, oligomers and charge states can be user-defined in the reference
file.

## Installation

### Source

You can install `lamp` from source. Download zip file and unzip somewhere in
your PC (Windows, Linux and MacOS) or git-clone this site. Go to `lamp`
directory and do:

```bash
cd lamp                              # go to 'lamp' folder
pip install .                        # install 'lamp' locally
lamp --help                          # check installation

# OPTION: update 'lamp' if you have already installed 'lamp'
pip install . --upgrade --no-deps
```

Or build `lamp` package locally and then install it:

```bash
pip install build                       # install 'build' package
cd lamp                                 # go to 'lamp' folder
python -m build                         # create 'lamp' package
cd dist                                 # go to 'lamp' package folder
pip install lamp-x.x.x.tar.gz           # install 'lamp'
```

You need to change 'x.x.x' to right version such as '1.0.0'.

### Conda

(coming soon)

### PyPI

(coming soon)

## Usages

For end users, `lamp` provides command line and graphical user interfaces.

    $ lamp --help
    Executing lamp version 1.0.0.
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
      --sep 'tab' \
      --input-data './data/df_pos_3.tsv' \
      --col-idx '1, 2, 3, 4' \
      --add-path '' \
      --ref-path '' \
      --ion-mode 'pos' \
      --cal-mass \
      --thres-rt '1.0' \
      --thres-corr '0.5' \
      --thres-pval '0.05' \
      --method "pearson" \
      --positive \
      --ppm '5.0' \
      --save-db \
      --save-mr \
      --db-out './res/test.db' \
      --sr-out './res/test_s.tsv' \
      --mr-out './res/test_m.tsv'

### Graphical user interface (GUI)

    $ lamp gui

## Authors

-   Wanchang Lin (<Wanchang.Lin@liverpool.ac.uk>)
-   Warwick Dunn (<Warwick.Dunn@liverpool.ac.uk>)
