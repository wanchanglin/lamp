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

### Source

You can install `LAMP` from source. Download zip file and unzip somewhere in
your PC (Windows, Linux and MacOS) or git-clone this site. For example,
clone this site for installation:

```bash
git clone https://github.com/wanchanglin/lamp.git  # clone this site
cd lamp                                            # go to 'LAMP' folder
pip install .                                      # install 'LAMP'. If no 'pip', try 'pip3'
lamp gui                                           # run 'LAMP' GUI
```

If you have already installed `LAMP`, you can use following to update:

```bash
cd lamp                            # go to 'LAMP'
git pull                           # update 'LAMP' repository
pip install . --upgrade            # Use 'pip3' if there is no 'pip'
```

### Conda

(coming soon)

### PyPI

(coming soon)

## Usages

For end users, `LAMP` provides command line and graphical user interfaces.

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

## Documentation

Documentation is hosted on [Read the Docs](https://lamp-liverpool-annotation-of-metabolite-using-mass-spectrometry.readthedocs.io/en/latest/).

## Authors

- Wanchang Lin (<Wanchang.Lin@liverpool.ac.uk>), The University of Liverpool
- Warwick Dunn (<Warwick.Dunn@liverpool.ac.uk>), The University of Liverpool
