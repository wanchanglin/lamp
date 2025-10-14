import os
import re
import sqlite3
import pandas as pd
import numpy as np
import janitor      # remove_empty()
from pyteomics import mass
from collections import OrderedDict
import lamp
from lamp.utils import (df2dict, flatten_cols, flatten_list)


# ------------------------------------------------------------------------
# wl-08-10-2024, Tue: merge single row summary with correlation analysis
def comp_summ_corr(sr, corr_df):
    """
    Merge annotation table with correlation analysis

    Parameters
    ----------
    sr : DataFrame
        A pandas data frame of annotation summary with single row and
        multiple column format.
    corr_df : DataFrame
        A pandas data frame of correlation group and its count.

    Returns
    -------
    DataFrame
        A data frame of combined annotation summary table.
    """

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

    res = pd.concat([res_1, res_2], ignore_index=True)

    return res


# ------------------------------------------------------------------------
# wl-14-05-2024, Tue: get summary table of compound annotation
def comp_summ(pk, comp, unique=False):
    """
    Get annotation summary table.

    Parameters
    ----------
    pk : DataFrame
        A pandas data frame of peak table. It must have "name", "mz" and
        "rt" columns.
    comp : DataFrame
        A pandas data frame of metabolite annotation.
    unique : bool
        A flag for using unique match or not

    Returns
    -------
    sr_mc : DataFrame
        A pandas dataframe with single row and multiple column table.
    mr_mc : DataFrame
        A pandas dataframe with multiple row and multiple column table.
    """

    mr_mc = (
        pk[["name", "mz", "rt"]]
        .merge(comp, left_on="name", right_on="id", how="outer",
               suffixes=('', '_remove'))
        .loc[:, lambda x: [i for i in x.columns if 'remove' not in i]]
        .drop(["id"], axis=1)
        # .sort_values(["name", "compound_id"], ignore_index=True)
    )

    ret = comp_merge(comp, unique=unique)
    sr_mc = (
        pk[["name", "mz", "rt"]]
        .merge(ret, left_on="name", right_on="name", how="outer",
               suffixes=('', '_remove'))
        .loc[:, lambda x: [i for i in x.columns if 'remove' not in i]]
    )

    return sr_mc, mr_mc


# ------------------------------------------------------------------------
# wl-20-05-2024, Mon: merge compound annotation
# wl-14-08-2024, Wed: give explanation of this function.
# wl-22-08-2024, Thu: add a flag for unique result or not
# wl-17-09-2025, Wed: add 'total_matching' for non-unique result
def comp_merge(comp, unique=False):
    """
    Merge compound annotation.

    This function merges all metabolite matches of a peak in single
    row for summary table.

    Parameters
    ----------
    comp : DataFrame
        A pandas data frame of metabolite match.
    unique : bool
        A flag for using unique match or not

    Returns
    -------
    DataFrame
        A pandas dataframe with merged columns.
    """
    # --------------------------------------------------------------------
    # Join string from a list
    # join_str(['ab', 'ab', 'efg', 'cd', 'efg', 'cd', 'efg', 'cd', 'efg'])
    def join_str(s):
        # s = [x for x in s if x]
        return '::'.join(s)

    # --------------------------------------------------------------------
    # Join unique string from a list
    # uni_str(['ab', 'ab', 'efg', 'cd', 'efg', 'cd', 'efg', 'cd', 'efg'])
    def uni_str(s):
        # s = [x for x in s if x]
        return '::'.join(list(set(s)))

    # -------------------------------------------------------------------
    # Count unique string from a list
    # uni_count(['ab', 'ab', 'efg', 'cd', 'efg', 'cd', 'efg', 'cd', 'efg'])
    def uni_count(s):
        # s = [x for x in s if x]
        return len(list(set(s)))

    # Get unique string and count or not
    if unique:
        tmp = (
            comp
            .select_dtypes(include='object')      # only select string
            .groupby("id")
            .agg([uni_str, uni_count])
            .pipe(flatten_cols)
            .rename(columns=lambda x: x.replace('_uni_str', ''))
            .rename(columns=lambda x: x.replace('_uni', ''))
            .rename_axis("name").reset_index()    # add rowname as a column
        )
    else:
        tmp_1 = (
            comp
            .select_dtypes(include='object')      # only select string
            # .drop("mz", axis=1)
            .groupby("id")
            # .groupby("id", as_index=False)
            .agg(join_str)
            .rename_axis("name").reset_index()    # add row-name as a column
        )
        # wl-17-09-2025, Wed: add matching count using apply on groupby
        tmp_2 = (
            comp
            .select_dtypes(include='object')      # only select string
            .groupby("id", group_keys=False)
            .apply(lambda x: x.shape[0], include_groups=False)
            .rename_axis("name").reset_index()    # add row-name as a column
            .rename(columns={0: "total_match"})
        )
        # merge two parts
        tmp = tmp_1.merge(tmp_2, on="name", how="left")

    # Get non-string columns
    # wl-15-08-2024, Thu: fix a bug
    num = list(comp.select_dtypes(exclude=['object']).columns)
    num.insert(0, "id")
    tmp1 = (
        comp
        .drop_duplicates('id', ignore_index=True)
        .loc[:, num]
        .rename(columns={'id': 'name'})
    )

    # merge two parts
    res = tmp1.merge(tmp, on="name", how="left")

    # Only select count columns for screen and return it?
    # tmp.filter(regex='_count$|^name', axis=1)

    return res


# ------------------------------------------------------------------------
# wl-14-05-2024, Tue: get summary of compound annotation
def _comp_summ_1(pk, comp):
    """
    Get annotation summary table.

    Parameters
    ----------
    pk : DataFrame
        A pandas data frame of peak table. It must have "name", "mz" and
        "rt" columns.
    comp : DataFrame
        A pandas data frame of metabolite annotation.

    Returns
    -------
    sr_mc : DataFrame
        A pandas dataframe with single row and multiple column table.
    mr_mc : DataFrame
        A pandas dataframe with multiple row and multiple column table.

    See Also
    --------
    comp_summ : Return two summary tables.

    Notes
    -----
    This is another version for metabolite annotation. And it does not call
    function `comp_merge`.
    """

    pk = pk[["name", "mz", "rt"]]

    mr_mc = (
        pk.merge(comp, left_on="name", right_on="id", how="outer",
                 suffixes=('', '_remove'))
        .loc[:, lambda x: [i for i in x.columns if 'remove' not in i]]
        .drop(["id"], axis=1)
        # .sort_values(["name", "compound_id"], ignore_index=True)
    )

    com = mr_mc.columns.to_list()
    com = [x for x in com if x not in
           ['name', 'mz', 'rt', 'exact_mass', 'ppm_error']]

    sr_mc = mr_mc.copy()

    sr_mc = (
        sr_mc
        # .fillna("")
        .assign(**{c: lambda x, y=c: x[y].astype(str) for c in com})
        .assign(
            **{c: lambda x, y=c: x.groupby("name")[y].transform("::".join)
               for c in com}
        )
        .drop_duplicates("name")
        .sort_values("name", ignore_index=True)
    )

    return sr_mc, mr_mc


# -------------------------------------------------------------------------
# wl-29-04-2024, Mon: Compound match without adducts library
# wl-06-08-2024, Tue: The only requirement from 'ref' is 'exact_mass'
def comp_match_mass(peak, ppm, ref):
    """
    Compound match.

    This function performs compound match against exact mass in reference
    library.

    Parameters
    ----------
    peak : DataFrame
        A pandas data frame of peak table. It must have "name", "mz" and
        "rt" columns.
    ppm : float
        A value for ppm.
    ref : DataFrame
        A pandas data frame of a library which must have `exact_mass` column.

    Returns
    -------
    DataFrame
        A pandas dataframe of compound match table.

    See Also
    --------
    com_match_mass_add : Return compound match table. This function uses a
        adducts library to adjust compound match.
    """

    # ---------------------------------------------------------------------
    # wl-29-04-2024, Mon: select compounds based on exact mass
    def comp_sel_mass(tab_name, col_names, cur, peak_id, mz, ppm):
        min, max = _cal_mass_tol(mz, ppm)
        rec = []
        cur.execute(
            """
            SELECT * from {} where exact_mass >= {} and exact_mass <= {}
            """.format(tab_name, min, max)
        )
        rec = [OrderedDict(zip(col_names, list(record)))
               for record in cur.fetchall()]
        for record in rec:
            record["id"] = peak_id
            record["mz"] = mz
            record["ppm_error"] = (mz - record["exact_mass"]) / (
                record["exact_mass"] * 0.000001
            )
        return rec

    # ---------------------------------------------------------------------
    # convert df to sql for speedy match
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    ref.to_sql(name='ref', con=con, if_exists="replace", index=False)
    con.commit()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tab_name = list(cur.fetchall())[0][0]
    # set index for fast query
    cur.execute(
        "CREATE INDEX idx_exact_mass ON {} (exact_mass)".format(tab_name))

    # get table column names
    if True:
        col_names = ref.columns.to_list()
    else:
        cur.execute("SELECT * FROM {}".format(tab_name))
        col_names = list(map(lambda x: x[0], cur.description))

    # convert peak list to dictionary for query
    pk = df2dict(peak[["name", "mz"]])

    # annotation/match compounds
    res = [comp_sel_mass(tab_name, col_names, cur, x, pk[x], ppm)
           for x in pk]
    res = flatten_list(res)
    res = pd.DataFrame(res)

    res = (
        res
        .round({"ppm_error": 2, "exact_mass": 2})
        # .sort_values(["id", "compound_id"], ignore_index=True)
        .drop_duplicates(ignore_index=True)
    )

    # move id and mz at the front
    cols_to_move = ['id', 'mz']
    res = res[cols_to_move +
              [x for x in res.columns if x not in cols_to_move]]

    # wl-17-09-2025, Wed: convert all ref as string
    cols = ref.columns.to_list()
    res = res.assign(**{c: lambda x, y=c: x[y].astype(str) for c in cols})

    con.close()

    return res


# -------------------------------------------------------------------------
# wl-24-04-2024, Wed: compound match
# Convert data frame 'ref' to sqlite for speedy query
# wl-06-08-2024, Tue: The only requirement from 'ref' is 'exact_mass'
# wl-07-08-2024, Wed: 'adduct' in peak has nothing to do with lib_adducts.
def comp_match_mass_add(peak, ppm, ref, lib_adducts):
    """
    Compound match.

    This function performs compound match against exact mass in reference
    library and adducts library.

    Parameters
    ----------
    peak : DataFrame
        A pandas data frame of peak table. It must have "name", "mz" and
        "rt" columns.
    ppm : float
        A value for ppm.
    ref : DataFrame
        A pandas data frame of reference library which must have
        `exact_mass` column.
    lib_adducts : DataFrame
        A pandas data frame of adducts library which must have `exact_mass`
        column.

    Returns
    -------
    DataFrame
        A pandas dataframe of compound match table.

    See Also
    --------
    com_match_mass : Return compound match table. This function does not use
        adducts library to adjust compound match.
    """

    # --------------------------
    # convert df to sql for speedy match
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    ref.to_sql(name='ref', con=con, if_exists="replace", index=False)
    con.commit()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tab_name = list(cur.fetchall())[0][0]
    # set index for fast query
    cur.execute(
        "CREATE INDEX idx_exact_mass ON {} (exact_mass)".format(tab_name))

    # get table column names
    if True:
        col_names = ref.columns.to_list()
    else:
        cur.execute("SELECT * FROM {}".format(tab_name))
        col_names = list(map(lambda x: x[0], cur.description))

    # --------------------------
    # convert peak list to dictionary for query
    pk = df2dict(peak[["name", "mz"]])
    # pk = peak.set_index('name').T.to_dict('records')[0]

    # convert lib_adducts to dictionary for query
    lib = (
        lib_adducts
        .rename(columns={"exact_mass": "mass"})
        # .set_index('label').T.to_dict('list')
        .set_index('label').T.to_dict('dict')
    )

    # annotation/match compounds
    res = [_comp_sel(lib, tab_name, col_names, cur, x, pk[x], ppm)
           for x in pk]
    res = flatten_list(res)
    res = pd.DataFrame(res)

    # clean up
    res = (
        res
        .round({"ppm_error": 2, "exact_mass": 2})
        # .sort_values(["id", "compound_id"], ignore_index=True)
        # .drop_duplicates(['id', 'compound_id'], ignore_index=True)
        .drop_duplicates(ignore_index=True)
    )

    # move id and mz at the front
    cols_to_move = ['id', 'mz']
    res = res[cols_to_move +
              [x for x in res.columns if x not in cols_to_move]]

    con.close()

    return res


# -------------------------------------------------------------------------
# wl-11-01-2024, Thu: select compounds based on exact mass
# wl-24-04-2024, Wed: use all column names
def _comp_sel(lib, tab_name, col_names, cur, peak_id, mz, ppm):
    """Internal function for `comp_match_mass_add`."""

    min_mz, max_mz = _cal_mass_tol(mz, ppm)
    adducts = lib.keys()

    rec = []
    for adduct in adducts:    # adduct = '[M+Mg]+'
        if min_mz - lib[adduct]["mass"] < 0.5:
            continue

        min = (min_mz - lib[adduct]["mass"]) * lib[adduct]["charge"]
        max = (max_mz - lib[adduct]["mass"]) * lib[adduct]["charge"]

        cur.execute(
            """
            SELECT * from {} where exact_mass >= {} and exact_mass <= {}
            """.format(tab_name, min, max)
        )

        sub = [OrderedDict(zip(col_names, list(record)))
               for record in cur.fetchall()]

        for record in sub:
            record["exact_mass"] = (
                record["exact_mass"] / lib[adduct]["charge"]
                + lib[adduct]["mass"]
            )
            record["adduct"] = adduct

        rec.extend(sub)

    for record in rec:
        record["id"] = peak_id
        record["mz"] = mz
        record["ppm_error"] = (mz - record["exact_mass"]) / (
            record["exact_mass"] * 0.000001
        )

    return rec


# -------------------------------------------------------------------------
# wl-22-04-2024, Mon: calculate mass tolerance/range based on ppm
# wl-11-10-2024, Fri: Review
def _cal_mass_tol(mass, ppm):
    """
    Calculate m/z value tolerance/range.

    Parameters
    ----------
    mass : float
        A mass value.
    ppm : float
        ppm value.

    Returns
    -------
    min_tol : float
        Minimal tolerance.
    max_tol : float
        Maximal tolerance.
    """

    delta = 0.000001
    min_tol = (1 - delta * ppm) * mass
    max_tol = (1 + delta * ppm) * mass

    return min_tol, max_tol


# -----------------------------------------------------------------------
# wl-22-04-2024, Mon: calculate molecular formula' exact mass
# wl-23-04-2024, Tue: fix a bug. use argument names for 'calculate_mass'
# wl-06-08-2024, Tue: exception handling. how to catch user-defined error:
#  PyteomicsError?
def _cal_mass(formula, mass_data):
    """
    Calculate molecular formula's exact mass

    Parameters
    ----------
    formula : str
        A string with a chemical formula.
    mass_data : OrderedDict
        A dict with the masses of the chemical elements.

    Returns
    -------
    float
        A mass value
    """

    formula = str(formula)
    try:
        res = mass.calculate_mass(formula=formula, mass_data=mass_data)
        # res = round(res, 6)
    # except (KeyError, PyteomicsError, NameError):
    except Exception:
        res = np.nan

    return res


# -----------------------------------------------------------------------
# wl-08-08-2024, Thu: adjust molecular formula' exact mass
# wl-06-11-2024, Wed: Re-write
def _adj_mass(mass, adduct, add_dict):
    """
    Adjust mass based on adduct library

    Parameters
    ----------
    mass : float
        Mass value to be adjusted.
    adduct : str
        A string of adduct. It is used to match against 'add_dict'.
    add_dict : dict
        A dictionary of adducts library.

    Returns
    -------
    float
        Adjusted mass
    """

    if adduct in add_dict:
        adj = mass + add_dict[adduct]
    else:
        adj = mass

    return adj


# -----------------------------------------------------------------------
# wl-22-04-2024, Mon: calculate exact mass for a reference data frame
# wl-07-08-2024, Wed: problem if adduct does not match in adduct library
# wl-08-08-2024, Thu: fix a bug in mass adjustment
def cal_mass(df, lib_adducts=None):
    """
    Calculate exact mass for an reference data frame.

    This function calculates exact mass using NIST database. If the
    reference file has 'adduct' column and user provides a adducts library,
    the exact mass will be adjust according to the adducts library.

    Parameters
    ----------
    df : DataFrame
        An reference data frame. It must have a column called
        'molecular_formula'.
    lib_adducts : DataFrame
        Adducts library in data frame format for mass adjustment. Only for
        'df' has 'ion_type' column.

    Returns
    -------
    DataFrame
        Reference dataframe with exact mass.
    """

    # --------------------------------------------------------------------
    def parse_nist_database(fn, skip_lines=10):
        """
        Parse NIST database.

        This function is called by `nist_database_to_pyteomics`.

        Parameters
        ----------
        fn : str
            Text file (NISTs Linearized ASCII Output)
        skip_lines : integer
            The number of lines of the data file to skip before beginning to
            read data.

        Yields
        ------
        Ordered dictionary
            Containing the parsed records

        Notes
        -----
        This function is from python package `beamspy`.
        """

        with open(fn, "r") as inp:
            for i in range(skip_lines):
                inp.readline()
            for e in inp.read().split("\n\n"):
                record = OrderedDict()
                for line in e.strip().split("\n"):
                    kv = line.split(" =")
                    if kv[0] == "Relative Atomic Mass":
                        record[kv[0]] = re.findall(r'\d+(?:\.\d+)?', kv[1])
                        record[kv[0]][0] = float(record[kv[0]][0])
                        record[kv[0]][1] = int(record[kv[0]][1])

                    elif kv[0] == "Isotopic Composition":
                        matches = re.findall(r'\d+(?:\.\d+)?', kv[1])
                        if len(matches) > 0:
                            record[kv[0]] = matches
                            if len(matches) > 1:
                                record[kv[0]][0] = float(record[kv[0]][0])
                                record[kv[0]][1] = int(record[kv[0]][1])
                            else:
                                record[kv[0]] = [float(record[kv[0]][0]), None]
                        else:
                            record[kv[0]] = [0.0, None]
                    elif kv[0] == "Atomic Number" or kv[0] == "Mass Number":
                        record[kv[0]] = int(kv[1])
                    elif kv[0] == "Standard Atomic Weight":
                        matches = re.findall(r'\d+(?:\.\d+)?', kv[1])
                        record[kv[0]] = matches
                    else:
                        record[kv[0]] = kv[1].strip()
                yield record

    # --------------------------------------------------------------------
    def nist_database_to_pyteomics(fn, skip_lines=10):
        """
        Convert NIST database to dict for calculation of mass

        Parameters
        ----------
        fn : str
            Text file (NISTs Linearized ASCII Output)
        skip_lines : integer
            The number of lines of the data file to skip before beginning to
            read data.

        Returns
        -------
        dict
            Ordered dictionary containing NIST records compatible with
            `Pyteomics`.

        Notes
        -----
        This function is from python package `beamspy`.
        """

        def add_record(r, nm):
            if r["Atomic Symbol"] not in nm:
                # update after all records have been added
                nm[r["Atomic Symbol"]] = OrderedDict([(0, (0.0, 0.0))])
                nm[r["Atomic Symbol"]][r["Mass Number"]] = (
                    r["Relative Atomic Mass"][0], r["Isotopic Composition"][0])
            else:
                nm[r["Atomic Symbol"]][r["Mass Number"]] = (
                    r["Relative Atomic Mass"][0], r["Isotopic Composition"][0])
            return nm

        def order_composition_by_hill(composition):
            symbols = set(composition)
            if 'C' in symbols:
                symbols.remove('C')
                yield 'C'
                if 'H' in symbols:
                    symbols.remove('H')
                    yield 'H'
            for symbol in sorted(symbols):
                yield symbol

        lib = OrderedDict()
        for record in parse_nist_database(fn, skip_lines=skip_lines):
            if record["Atomic Symbol"] in ["D", "T"]:
                lib = add_record(record, lib)
                record["Atomic Symbol"] = "H"
                lib = add_record(record, lib)
            else:
                lib = add_record(record, lib)

        for element in list(lib.keys()):
            lib_sorted = sorted(lib[element].items(),
                                key=lambda e: e[1][1], reverse=True)
            if lib_sorted[0][1][0] > 0.0:
                lib[element][0] = (lib_sorted[0][1][0], 1.0)
            elif len(lib_sorted) == 2:
                lib[element][0] = (lib_sorted[1][1][0], 1.0)
            else:
                del lib[element]

        es = list(order_composition_by_hill(lib.keys()))

        return OrderedDict((k, lib[k]) for k in es)

    # --------------------------------------------------------------------
    nist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'lib', 'nist_database.txt')
    nist_mass = nist_database_to_pyteomics(nist_path)

    # get exact mass
    df = (
        df
        # wl-08-08-2024, Thu: use Series's apply here for single columns
        .assign(exact_mass=lambda x:
                x.molecular_formula.apply(_cal_mass, mass_data=nist_mass))
    )

    # adjust exact mass or not
    if ("adduct" in df.columns) and (lib_adducts is not None):
        # convert 2-column df into dictionary for speedy query
        add = df2dict(lib_adducts.iloc[:, 0:2])
        df = (
            df
            # wl-08-08-2024, Thu: use df's apply here with multiple columns
            #  and cell-wise custom function.
            .assign(exact_mass=lambda x: x.apply(
                lambda x: _adj_mass(x.exact_mass, x.adduct, add), axis=1))
        )

    return df


# ------------------------------------------------------------------------
# wl-22-04-2024, Mon: load reference file for compound annotation
# wl-08-08-2024, Thu: use 'cal_mass' function
# wl-10-09-2024, Tue: remove empty rows and columns
# wl-11-09-2024, Wed: rename 'name' as 'molecular_name' in case 'name'
#   conflicts with data set's peak 'name'.
# wl-09-10-2024, Wed: set 'filename' default value
# wl-23-10-2024, Wed: support Excel
# wl-30-10-2024, Wed: add ion_mode
def read_ref(fn="", ion_mode="pos", sheet_name=0, sep="\t", calc=False,
             lib_adducts=None):
    """
    Load reference for compound annotation

    Parameters
    ----------
    fn : str
        Full path for an reference file. If empty, use default reference
        file. This file must have `formula` or `molecular_formula` column.
        The current supported file formats are text formats (csv, tsv, txt
        and dat) and Excel formats (xls, xlsx).
    ion_mode : str
        A string for ion mode, "pos" or "neg".
    sheet_name: str or int
        This argument is used for Excel file format. Strings are used for
        sheet names. Integers are used in zero-indexed sheet positions
        (chart sheets do not count as a sheet position).

        Available cases:

        * Defaults to ``0``: 1st sheet as a `DataFrame`
        * ``1``: 2nd sheet as a `DataFrame`
        * ``"Sheet1"``: Load sheet with name "Sheet1"

    sep : str
        Character to treat as the delimiter. It is used for text file
        format.
    calc : bool
        Calculate exact mass or not.
    lib_adducts : DataFrame
        Adducts library in data frame format for mass adjustment. Only for
        'fn' has 'ion_type' column.

    Returns
    -------
    DataFrame
        Reference dataframe with exact mass.

    Notes
    -----
    This function will remove reference empty rows and columns.
    """

    # load default reference library
    if not fn:
        path = 'lib/GSMM_LAMP_ReferenceFile_v1_281024.xlsx'
        fn = os.path.join(
            os.path.dirname(os.path.abspath(lamp.__file__)), path
        #     os.path.dirname(os.path.abspath(__file__)), path
        )

    ext = os.path.splitext(fn)[1][1:]
    if ext in ['xls', 'xlsx']:
        df = pd.read_excel(fn, sheet_name=sheet_name, header=0)
    elif ext in ['txt', 'csv', 'tsv', 'dat']:
        df = pd.read_table(fn, header=0, sep=sep)
    else:
        raise ValueError("Data must be: xls, xlsx, txt, csv, tsv or dat.")

    # tidy up
    df = df.remove_empty().clean_names()

    # rename if possible
    if "molecular_formula" not in df.columns:
        df = df.rename(columns={"formula": "molecular_formula"})
    if "compound_name" not in df.columns:
        df = df.rename(columns={"name": "compound_name"})
    if "exact_mass" not in df.columns and "m_z" in df.columns:
        df = df.rename(columns={"m_z": "exact_mass"})
    else:
        df = df.rename(columns={"ion_m_z": "exact_mass"})

    # reference file must have either "molecular_formula" or "exact_mass",
    # or both
    if ("molecular_formula" not in df.columns) and (
            "exact_mass" not in df.columns):
        raise ValueError("Input data must have 'molecular_formula' or"
                         " 'exact_mass' columns")

    # df = df.reorder_columns(['molecular_formula', 'molecular_name'])

    if ('exact_mass' in df.columns) and (df.exact_mass.dtype != "float64"):
        df = df.assign(exact_mass=lambda x: x["exact_mass"].astype(float))

    if "ion_mode" in df and ion_mode:
        # 30-10-2024, Wed: use regex for case-insensitive and partial match
        idx = df['ion_mode'].str.contains(ion_mode, case=False)
        if idx.sum() > 0:
            df = df[idx]
        else:
            raise ValueError("Ion mode must be pos/positive or neg/negative.")

    # calculate exact mass
    if calc or ('exact_mass' not in df.columns):
        df = cal_mass(df, lib_adducts)

    return df


# -------------------------------------------------------------------------
# wl-24-12-2023, Sun: get library in data frame format
# wl-09-10-2024, Wed: set 'filename' default value
# wl-30-10-2024, Wed: minor changes
def read_lib(fn="", ion_mode="pos", sheet_name=0, sep="\t"):
    """
    Load adducts library file.

    Parameters
    ----------
    fn : str
        Full path for an library file. if empty, use default library file.
    ion_mode : str
        A string for ion mode, "pos" or "neg".
    sheet_name: str or int
        This argument is used for Excel file format. Strings are used for
        sheet names. Integers are used in zero-indexed sheet positions
        (chart sheets do not count as a sheet position).

        Available cases:

        * Defaults to ``0``: 1st sheet as a `DataFrame`
        * ``1``: 2nd sheet as a `DataFrame`
        * ``"Sheet1"``: Load sheet with name "Sheet1"

    sep : str
        File delimiter, `\t` or `,`.

    Returns
    -------
    DataFrame
        A library data frame.
    """

    # load default library
    if not fn:
        path = 'lib/adducts.txt'
        fn = os.path.join(
            os.path.dirname(os.path.abspath(lamp.__file__)), path
        #     os.path.dirname(os.path.abspath(__file__)), path
        )
        sep = "\t"

    ext = os.path.splitext(fn)[1][1:]
    if ext in ['xls', 'xlsx']:
        df = pd.read_excel(fn, sheet_name=sheet_name, header=0)
    elif ext in ['txt', 'csv', 'tsv', 'dat']:
        df = pd.read_table(fn, header=0, sep=sep)
    else:
        raise ValueError("Data must be: xls, xlsx, txt, csv, tsv or dat.")

    if "ion_mode" in df.columns and ion_mode:
        # 30-10-2024, Wed: use regex for case-insensitive and partial match
        idx = df['ion_mode'].str.contains(ion_mode, case=False)
        # idx = (df["ion_mode"] == ion_mode)
        if idx.sum() > 0:
            df = df[idx]

    df = df.drop("ion_mode", axis=1)

    return df


# --------------------------------------------------------------------------
# wl-21-09-2022, Wed: Read file consisting of peak list and data matrix.
# wl-02-09-2024, Mon: add 'dat' format for Galaxy data extension
# wl-10-10-2024, Thu: remove calculation of intensity average
def read_peak(fn, cols=[1, 2, 3, 4], sheet_name=0, sep="\t"):
    """
    Read metabolite data.

    The file must have peak-list and intensity data and must be one of file
    formats: xls, xlsx, txt, csv and tsv.

    Parameters
    ----------
    fn : str
        File name.
    cols : list
        A list indicating column index of 'name', 'mz', 'rt' and start of
        intensity data matrix.
    sheet_name: str or int
        This argument is used for Excel file format. Strings are used for
        sheet names. Integers are used in zero-indexed sheet positions
        (chart sheets do not count as a sheet position).

        Available cases:

        * Defaults to ``0``: 1st sheet as a `DataFrame`
        * ``1``: 2nd sheet as a `DataFrame`
        * ``"Sheet1"``: Load sheet with name "Sheet1"

    sep : str
        File separator for txt, csv and tsv file. `\t` or `,`.

    Returns
    -------
    DataFrame
        A data frame with the first 3 columns as name, mz and rt.
    """

    ext = os.path.splitext(fn)[1][1:]
    if ext in ['xls', 'xlsx']:
        data = pd.read_excel(fn, sheet_name=sheet_name, header=0)
    elif ext in ['txt', 'csv', 'tsv', 'dat']:
        data = pd.read_table(fn, header=0, sep=sep)
    else:
        raise ValueError("Data must be: xls, xlsx, txt, csv, tsv or dat.")

    # data = pd.read_table(fn, header=0, sep=sep)

    # get python index
    cols = [x - 1 for x in cols]
    # cols = list(map(lambda x: x - 1, cols))

    # get peak list
    peak = data.iloc[:, cols[:3]]

    # get intensity
    mat = data.iloc[:, cols[-1]:]

    # column bind ('cbind' in R)
    data = pd.concat([peak, mat], axis=1, ignore_index=False)

    data.rename(columns={data.columns[0]: 'name',
                         data.columns[1]: 'mz',
                         data.columns[2]: 'rt'},
                inplace=True)
    data['name'] = data['name'].astype(str)

    # replace 0 with na for the future correlation analysis
    data.replace(0, np.nan, inplace=True)

    return data
