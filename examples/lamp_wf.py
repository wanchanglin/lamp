#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wl-29-08-2024, Thu: lamp command-line workflow
# wl-03-09-2024, Tue: tidy up

import os
import sqlite3
import pandas as pd
import lamp as mt


# -------------------------------------------------------------------------
def lamp_cmd(para):

    para = pd.Series(para)

    # ---------------------------------------------------------------------
    # get libraries for peak feature annotation

    if not para['add_path']:
        path = 'lib/adducts.txt'
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        para['add_path'] = p

    if not para['ref_path']:
        path = 'lib/db_compounds.txt'
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        para['ref_path'] = p

    # ---------------------------------------------------------------------
    # get data with peak list and intensity matrix
    df = mt.read_peak(para['data_path'], cols=para['name_col':'data_col'],
                      sep=para['sep'])

    # ---------------------------------------------------------------------
    # calculate exact mass
    ref = mt.read_ref(para['ref_path'], calc=para['cal_mass'])

    # ---------------------------------------------------------------------
    # match compound based on exact mass
    if para['add_mass']:
        # match compounds with adduct library mass adjustment
        lib_add = mt.read_lib(para['add_path'], para['ion_mode'])
        match = mt.comp_match_mass_add(df, para['ppm'], ref, lib_add)
    else:
        # match compounds without adduct library mass adjustment
        match = mt.comp_match_mass(df, para['ppm'], ref)

    # ---------------------------------------------------------------------
    # correlation analysis with corr, pval and rt_diff
    print("***Correlation analysis.***\n")
    mt._tic()
    corr = mt.comp_corr_rt(df,
                           thres_rt=para['thres_rt'],
                           thres_corr=para['thres_corr'],
                           thres_pval=para['thres_pval'],
                           method=para['method'],
                           positive=para['positive'])
    mt._toc()
    print("\n***Correlation analysis: Done.***")

    # get correlation group and size
    print("\n***Get correlation group and size.***")
    mt._tic()
    corr_df = mt.corr_grp_size(corr)
    mt._toc()
    print("\n***Get correlation group and size: Done.***")

    # ---------------------------------------------------------------------
    # get summary of metabolite annotation
    sr, mr = mt.comp_summ(df, match)

    # merge summery table with correlation analysis
    res = (
        sr.merge(corr_df, left_on="name", right_on='name', how="left")
        .sort_values(["cor_grp_size"], ignore_index=True, ascending=False)
    )

    # sort out based on correlation group and compound matches
    idx = res.ppm_error.notnull() & res.cor_grp_size.notnull()
    # split into two groups
    res_1 = res[idx]
    res_2 = res[~idx].sort_values(["ppm_error"])

    # combine again
    res = pd.concat([res_1, res_2], ignore_index=False)

    # ---------------------------------------------------------------------
    # get file name for results

    # extract data file name and path
    tmp = os.path.basename(para['data_path'])
    tmp = os.path.splitext(tmp)[0]

    # wl-30-08-2024, Fri: decide where the result to go. change here.
    # dir = os.path.dirname(para['data_path'])
    dir = os.path.dirname(os.path.abspath(__file__)) + '/res'

    # results full names
    db_out = dir + "/" + tmp + "_lamp" + ".db"
    sr_out = dir + "/" + tmp + "_lamp" + "_s.tsv"
    mr_out = dir + "/" + tmp + "_lamp" + "_m.tsv"

    # ---------------------------------------------------------------------
    # save all results to a sqlite database or not
    if para['save_db']:
        conn = sqlite3.connect(db_out)
        df[["name", "mz", "rt"]].to_sql("peaklist", conn,
                                        if_exists="replace", index=False)
        corr_df.to_sql("corr_grp", conn, if_exists="replace", index=False)
        corr.to_sql("corr_pval_rt", conn, if_exists="replace", index=False)
        match.to_sql("match", conn, if_exists="replace", index=False)
        mr.to_sql("anno_mr", conn, if_exists="replace", index=False)
        res.to_sql("anno_sr", conn, if_exists="replace", index=False)

        conn.commit()
        conn.close()

    # save multiple row results or not
    if para['save_mr']:
        mr.to_csv(mr_out, sep=para['sep'], index=False)

    # save results
    res.to_csv(sr_out, sep=para['sep'], index=False)

    return


# -------------------------------------------------------------------------
def main():

    # --------------------------
    # User's parameters setting
    # --------------------------
    # NOTE: Empty setting to use LAMP default values
    #  'ref_path': ""    # reference file for compound match
    #  'add_path': ""    # adduct mass library for compound match adjustment

    para = {
        # 1.) data name and column index of name, mz, rt and data begin
        'sep': "\t",                  # file separator: '\t' or ','
        # 'data_path': "./data_wl/df_pos_3.tsv",
        'data_path': "./res/Bunce_Lipids_Pos.tsv",
        'name_col': 1,                 # index of 'name' in 'data_path'
        'mz_col': 2,                   # index of 'mz' in 'data_path'
        'rt_col': 5,                   # index of data string in 'data_path'
        'data_col': 13,

        # 2.) feature grouping with correlation analysis
        'thres_rt': 1.0,       # threshold of RT difference
        'thres_corr': 0.7,     # threshold of correlation coefficient
        'thres_pval': 0.05,    # threshold of correlation p-values
        'method': "spearman",  # correlation method: pearson or spearman
        'positive': True,      # use positive correlation only

        # 3.) compounds annotation with reference and adduct files
        'ppm': 5,              # ppm value threshold
        'ion_mode': "pos",     # Ion mode of data set.
        'ref_path': "./databases/ref_all_v7_pos.tsv",
        # 'ref_path': "./databases/kegg_full_20210111_v1.tsv",
        # 'ref_path': "./databases/lipidmaps_full_20201001_v1.tsv",
        # 'ref_path': "",      # default reference file for compound match
        'cal_mass': False,     # calculate mass based on NIST database
        'add_mass': False,     # match compound with adduct mass adjustment
        # 'add_path': "",      # Adducts library for compound match mass
                               # adjustment.
        'add_path': "./lib/adducts.txt",

        # 4.) results outcome
        'save_db': True,       # save all results in sqlite database
        'save_mr': True,       # save multiple row result
    }

    # -----------
    # run lamp
    # -----------
    lamp_cmd(para)
    print(para['data_path'], "****Done****")


# -------------------------------------------------------------------------
if __name__ == '__main__':
    # mt._tic()
    main()
    # mt._toc()
