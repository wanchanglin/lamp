# # Quick Start
#
# In this vignette we will demonstrate how to use `LAMP` python package. The
# input data and reference files are located in
# https://github.com/wanchanglin/lamp/tree/master/examples/data.

# ## Setup
#
# To use `LAMP`, the first step is to import some python libraries including
# `LAMP`.

import sqlite3
import pandas as pd
from lamp import anno, stats, utils

# ## Data Loading
#
# `LAMP` supports text files separated by comma (`,`) or tab (`\t`).  The
# Microsoft's XLSX is also supported, using argument `sheet_name` to
# indicate which sheet is used for input data. The default is 0 for the
# first sheet.
#
# Here we use a small example data set with `tsv` format. Load it into
# python and check its format:
#

d_data = "./data/df_pos_2.tsv"
data = pd.read_table(d_data, header=0, sep="\t")
data

# This data set includes peak list and intensity data matrix. `LAMP`
# requires peak list's name, m/z value and retention time. User needs to
# indicate the locations of feature name, m/z value, retention time and
# starting points of data matrix from data. Here they are 1, 3, 6 and 11,
# respectively.
#
# Load input data with `xlsx` format for `LAMP`:

cols = [1, 3, 6, 11]
# d_data = "./data/df_pos_2.tsv"
# df = anno.read_peak(d_data, cols, sep='\t')
d_data = "./data/df_pos_2.xlsx"                      # use xlsx file
df = anno.read_peak(d_data, cols, sheet_name=0)
df

# The argument `sep` will be ignored if the input data is an `xlsx` file.
# Data frame `df` now includes only `name`, `mz`, `rt` and intensity data
# matrix.
#
# ## Metabolite Annotation
#
# To perform metabolite annotation, users should provide their own
# reference file. Otherwise, `LAMP` will use its default reference file for
# annotation. Here we load the default reference file for compound
# annotation. Since the input data is positive mode here, we only
# use positive part of reference file. If `ion_mode` is empty, all reference
# items will be used for matching.

ion_mode = "pos"
ref_path = ""  # if empty, use default reference file for matching
# load reference library
cal_mass = False
ref = anno.read_ref(ref_path, ion_mode=ion_mode, calc=cal_mass)
ref

# The reference file must have one column: `molecular_formula` (or
# `formula`) if there is no column called `ion m/z` (or, `m/z`,
# `exact_mass`). The `exact_mass` is optional. if absent, `LAMP` will use
# `molecular_formula` to calculate 'exact_mass' based on the NIST Atomic
# Weights and Isotopic Compositions for All Elements. If your reference file
# has `exact_mass` and you still want to calculate it using NIST database,
# set `calc` as True.  The `exact_mass` is used to match against a range of
# `mz`, controlled by `ppm`, in data frame `df`.
#
# As the same as input data, the reference file can be `xlsx` file. Another
# reference file is HMDB database for urine:

ref_path = "./data/hmdb_urine_v4_0_20200910_v1.tsv"
ref = anno.read_ref(ref_path, calc=True)
ref

# Next we use HMDB reference file for compounds match. Here function argument
# `ppm` is used to control the m/z matching tolerance(range).

ppm = 5.0
match = anno.comp_match_mass(df, ppm, ref)
match

# `match` gives the compound matching results. `LAMP` also provides a mass
# adjust option by adduct library. You can provide your own adducts library
# otherwise `LAMP` uses its default adducts library.
#
# The adducts library's format looks like:

add_path = './data/adducts_short.tsv'
lib_df = pd.read_csv(add_path, sep="\t")
lib_df

# The adducts library must have columns of `label`, `exact_mass`, `charge`
# and `ion_mode`.
#
# We use this adducts file to adjust mass:

# if empty, use default adducts library
add_path = "./data/adducts_short.tsv"
lib_add = anno.read_lib(add_path, ion_mode)
lib_add

# Now use function `comp_match_mass_add` to match compounds:

match_1 = anno.comp_match_mass_add(df, ppm, ref, lib_add)
match_1

# Note that this adducts library is also used to adjust mass calculation in
# loading reference file if there is a column called `ion_type`.
#
# ## Correlation Analysis
#
# Next step is correlation analysis, based on intensity data matrix along all
# peaks. All results are filtered by the correlation coefficient, p-values
# and retention time difference. That is: keep correlation results in an
# retention time differences/window (such as 1 second) with correlation
# coefficient larger than a threshold (such as 0.5) and their correlation
# p-values less than a threshold (such as 0.05).
#
# `LAMP` supports two correlation methods, `pearson` and `spearman`. Also
# parameter `positive` allows user to select only positive correlation
# results, otherwise positive and negative correlations will be used.
#
# Two functions, `_tic` and `_toc`, record the correlation computation time in
# seconds.

thres_rt = 1.0
thres_corr = 0.5
thres_pval = 0.05
method = "spearman"  # "pearson"
positive = True

utils._tic()
corr = stats.comp_corr_rt(df, thres_rt, thres_corr, thres_pval, method,
                          positive)
utils._toc()
corr

# `corr` gives results of correlation coefficient(`r_value`), correlation
# p-values(`p_value`) and retention time difference(`rt_diff`).
#
# Based on the correlation analysis, we can extract the groups and their
# sizes by:

# get correlation group and size
corr_df = stats.corr_grp_size(corr)
corr_df

# ## Summarize Results
#
# The final step gets the summary table in different format and save for the
# further analysis.

# get summary of metabolite annotation
sr, mr = anno.comp_summ(df, match)

# This function combines peak table with compound matching results and
# returns two results in different formats. `sr` is single row results for
# each peak id in peak table `df`:

sr

# `mr` is multiple rows format if the match more than once from the reference
# file:

mr

#
# Now we merges single format results with correlation results:
#

# merge summery table with correlation analysis
res = anno.comp_summ_corr(sr, corr_df)
res

# The result data frame `res` is re-arranged as four parts from top to bottom:
#
#  - 1st part: identified metabolites, satisfied with correlation analysis
#  - 2nd part: identified metabolites, not satisfied with correlation
#  - 3rd part: no identified metabolites, satisfied with correlation
#  - 4th part: no identified metabolites, not satisfied with correlation
#
# The users should focus on the first part and perform their further analysis.

# You can save all results in different forms, such as text format TSV or CSV.
# You can also save all results into a `sqlite3` database and use
# [DB Browser for SQLite](https://sqlitebrowser.org/) to view:

f_save = False          # here we do NOT save results
db_out = "test.db"
sr_out = "test_s.tsv"

if f_save:
    # save all results into a sqlite3 database
    conn = sqlite3.connect(db_out)
    df[["name", "mz", "rt"]].to_sql("peaklist",
                                    conn,
                                    if_exists="replace",
                                    index=False)
    corr_df.to_sql("corr_grp", conn, if_exists="replace", index=False)
    corr.to_sql("corr_pval_rt", conn, if_exists="replace", index=False)
    match.to_sql("match", conn, if_exists="replace", index=False)
    mr.to_sql("anno_mr", conn, if_exists="replace", index=False)
    res.to_sql("anno_sr", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    # save final results
    res.to_csv(sr_out, sep="\t", index=False)

# ## End User Usages
#
# For end users, `LAMP` provides two computation options: command line
# interface(CLI) and graphical user interface (GUI).
#
# To use GUI,  you need to open a terminal and type in:
#
# ```bash
# $ lamp gui
# ```
#
# To use CLI, open a terminal and type in command with required arguments,
# something like:
#
# ```bash
# $ lamp cli \
#   --input-data "./data/df_pos_3.tsv" \
#   --sep "tab" \
#   --col-idx "1, 2, 3, 4" \
#   --add-path "" \
#   --ref-path "" \
#   --ion-mode "pos" \
#   --cal-mass \
#   --thres-rt "1.0" \
#   --thres-corr "0.5" \
#   --thres-pval "0.05" \
#   --method "pearson" \
#   --positive \
#   --ppm "5.0" \
#   --save-db \
#   --save-mr \
#   --db-out "./res/test.db" \
#   --sr-out "./res/test_s.tsv" \
#   --mr-out "./res/test_m.tsv"
# ```
#
# For the best practice, you can create a bash script `.sh` (Linux
# and MacOS) or Windows script `.bat` to contain these CLI
# arguments. Change parameters in these files each time when processing new
# data set.
#
# For example, there are `lamp_cli.sh` and `lamp_cli.bat` in
# https://github.com/wanchanglin/lamp/tree/master/examples. You can run them
# and check the results in directory `examples/res`:
#
# - For Linux and MacOS terminal:
#
#   ```bash
#   $ chmod +x lamp_cli.sh
#   $ ./lamp_cli.sh
#   ```
#
# - For Windows terminal:
#
#   ```bash
#   $ lamp_cli.bat
#   ```
#
# Note that if users use `xlsx` files for input data and reference file
# when using GUI or CLI, all data must be in the first sheet. If you use
# `LAMP` functions in your python scripts, there are no such requirementss.
