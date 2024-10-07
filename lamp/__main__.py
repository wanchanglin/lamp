#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wl-07-10-2024, Mon: commence

# from lamp import __version__
import argparse
import sys
import os
import sqlite3
import pandas as pd
from PySide6.QtWidgets import QApplication
import lamp.lamp_gui as gui
import lamp.lamp as lamp


# --------------------------------------------------------------------------
def main():
    separators = {"tab": "\t", "comma": ","}

    print("Executing lamp version {}.".format(__version__))

    parser = argparse.ArgumentParser(
        description='Compounds Annotation of LC-MS data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(dest='step')
    parser_am = subparsers.add_parser('cmd',
                                      help='Annotate metabolites in CMD.')
    parser_gui = subparsers.add_parser('gui',
                                       help='Annotate metabolites in GUI.')

    # ---------------------------------------------------------------------
    # data loading
    parser_am.add_argument('--input-data', type=str, required=True,
                           help="Data set including peak-list.")
    parser_am.add_argument('--col-idx', default="1,2,3,4", type=str,
                           help='Column index of name, mz, rt and start of data intensity')
    parser_am.add_argument('--sep', default="tab", type=str,
                           choices=["tab", "comma"],
                           help="Values in input or output file are " \
                                   "separated by this character.")

    # ---------------------------------------------------------------------
    # feature grouping with correlation analysis
    parser_am.add_argument('--thres-rt', default=1.0, type=float,
                           help="Threshold of retension time difference.")
    parser_am.add_argument('--thres-corr', default=0.5, type=float,
                           help="Threshold of correlation coefficient.")
    parser_am.add_argument('--thres-pval', default=0.05, type=float,
                           help="Threshold of correlation p-values.")
    parser_am.add_argument('--method', default="pearson", type=str,
                           choices=["pearson", "spearman"],
                           help="Correlation method.")
    parser_am.add_argument('--positive', action='store_true',
                           help="Positive corelation coefficients or not.")

    # ---------------------------------------------------------------------
    # compounds annotation with reference and adduct files
    parser_am.add_argument('--ppm', default=5.0, type=float,
                           help="Mass tolerance in parts per million.")
    parser_am.add_argument('--ion-mode', default='pos', type=str,
                           choices=["pos", "neg"], help="Ion mode of data set.")
    parser_am.add_argument('--ref-path', type=str, default=None, required=False,
                           help="Reference file for compound matching.")
    parser_am.add_argument('--cal-mass', action="store_true",
                           help="Calculate mass based on NIST database.")
    parser_am.add_argument('--add-mass', action="store_true",
                           help="Match compound with adduct mass adjustment.")
    parser_am.add_argument('--add-path', type=str, default=None, required=False,
                           help="Adducts library for compound match mass adjustment.")

    # ---------------------------------------------------------------------
    # results outcome
    parser_am.add_argument('--save-db', action="store_true",
                           help="Save all results in a sql database.")
    parser_am.add_argument('--save-mr', action="store_true",
                           help="Save multiple row result.")

    parser_am.add_argument('--db-out', type=str, required=True,
                           help="All results saved in a sqlite database.")
    parser_am.add_argument('--sr-out', type=str, required=True,
                           help="Compound annotation reseults")
    parser_am.add_argument('--mr-out', type=str, required=True,
                           help="Compound annotation results in mutiple row format")

    # ---------------------------------------------------------------------
    args = parser.parse_args()
    print(args)

    if args.step == "cmd":

        # -----------------------------------------------------------------
        # load libraries for annotation
        if not args.add_path:
            path = 'lib/adducts.txt'
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
            args.add_path = p

        if not args.ref_path:
            path = 'lib/db_compounds.txt'
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
            args.ref_path = p

        # -----------------------------------------------------------------
        # get data with peak list and intensity matrix
        idx_list = [int(item.strip()) for item in args.col_idx.split(',')]
        df = lamp.read_peak(fn=args.input_data, cols=idx_list,
                        sep=separators[args.sep])

        # -----------------------------------------------------------------
        # calculate exact mass
        ref = lamp.read_ref(args.ref_path, calc=args.cal_mass)

        # -----------------------------------------------------------------
        # match compound based on exact mass
        if args.add_mass:
            # match compounds with adduct library mass adjustment
            lib_add = lamp.read_lib(args.add_path, args.ion_mode)
            match = lamp.comp_match_mass_add(df, args.ppm, ref, lib_add)
        else:
            # match compounds without adduct library mass adjustment
            match = lamp.comp_match_mass(df, args.ppm, ref)

        # -----------------------------------------------------------------
        # correlation analysis with corr, pval and rt_diff
        corr = lamp.comp_corr_rt(df,
                            thres_rt=args.thres_rt,
                            thres_corr=args.thres_corr,
                            thres_pval=args.thres_pval,
                            method=args.method,
                            positive=args.positive)

        # get correlation group and size
        corr_df = lamp.corr_grp_size(corr)

        # -----------------------------------------------------------------
        # get summary of metabolite annotation
        sr, mr = lamp.comp_summ(df, match)

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

        # -----------------------------------------------------------------
        # save all results to a sqlite database or not
        if args.save_db:
            conn = sqlite3.connect(args.db_out)
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
        if args.save_mr:
            mr.to_csv(args.mr_out, sep=separators[args.sep], index=False)

        # save results
        res.to_csv(args.sr_out, sep=separators[args.sep], index=False)

    if args.step == "gui":
        # Exception Handling
        try:
            app = QApplication(sys.argv)
            form = gui.lamp_app()
            form.show()
            sys.exit(app.exec())
        except NameError:
            print("Name Error:", sys.exc_info()[1])
        except SystemExit:
            print("Closing Window...")
        except Exception:
            print(sys.exc_info()[1])


# -------------------------------------------------------------------------
if __name__ == '__main__':
    main()
