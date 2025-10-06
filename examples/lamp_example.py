# wl-08-10-2024, Tue: LAMP example
from lamp import anno, stats, utils

# =========================================================================
# data set
d_data = "./data/df_pos_3.tsv"
cols = [1, 2, 3, 4]

df = anno.read_peak(d_data, cols, sep='\t')
df

# ========================================================================
# metabolite annotation: match the exact mass
ppm = 5.0
ion_mode = "pos"
add_path = ""
ref_path = ""
# ref_path = "./data/hmdb_urine_v4_0_20200910_v1.tsv"
# ref_path = "./data/kegg_full_20210111_v1.tsv"
# ref_path = "./data/biocyc_chlamycyc_20180702_v1.tsv"
cal_mass = True
add_mass = False

# load reference library
ref = anno.read_ref(ref_path, ion_mode, calc=cal_mass)
ref

if add_mass:
    # match compounds with adduct library mass adjustment
    lib_add = anno.read_lib(add_path, ion_mode)
    match = anno.comp_match_mass_add(df, ppm, ref, lib_add)
else:
    # match compounds without adduct library mass adjustment
    match = anno.comp_match_mass(df, ppm, ref)
match
match.columns

# ========================================================================
# correlation analysis with corr, pval and rt_diff
thres_rt = 1.0
thres_corr = 0.7
thres_pval = 0.05
method = "spearman"   # "pearson"
positive = True

utils._tic()
corr = stats.comp_corr_rt(df, thres_rt, thres_corr, thres_pval, method,
                          positive)
utils._toc()
corr

# get correlation group and size
corr_df = stats.corr_grp_size(corr)
corr_df

# ========================================================================
# get summary of metabolite annotation
sr, mr = anno.comp_summ(df, match)
sr
mr

# merge summery table with correlation analysis
res = anno.comp_summ_corr(sr, corr_df)
res
