# wl-17-04-2024, Wed: commence.
import os
import re
import time
import sqlite3
import scipy
import pandas as pd
import numpy as np
from pyteomics import mass
from collections import OrderedDict


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
        a flag for using unique match or not

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
        a flag for using unique match or not

    Returns
    -------
    DataFrame
        A pandas dataframe with merged columns.
    """
    # --------------------------------------------------------------------
    # Join string from a list
    # join_str(['ab', 'ab', 'efg', 'cd', 'efg', 'cd', 'efg', 'cd', 'efg'])
    def join_str(s):
        s = [x for x in s if x]
        return '::'.join(s)

    # --------------------------------------------------------------------
    # Join unique string from a list
    # uni_str(['ab', 'ab', 'efg', 'cd', 'efg', 'cd', 'efg', 'cd', 'efg'])
    def uni_str(s):
        s = [x for x in s if x]
        return '::'.join(list(set(s)))

    # -------------------------------------------------------------------
    # Count unique string from a list
    # uni_count(['ab', 'ab', 'efg', 'cd', 'efg', 'cd', 'efg', 'cd', 'efg'])
    def uni_count(s):
        s = [x for x in s if x]
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
        tmp = (
            comp
            .select_dtypes(include='object')      # only select string
            # .drop("mz", axis=1)
            .groupby("id")
            # .groupby("id", as_index=False)
            .agg(join_str)
            .rename_axis("name").reset_index()    # add rowname as a column
        )

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
        min, max = cal_mz_tol(mz, ppm)
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

    min_mz, max_mz = cal_mz_tol(mz, ppm)
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
        res = round(res, 6)
    # except (KeyError, PyteomicsError, NameError):
    except Exception:
        res = np.nan

    return res


# -----------------------------------------------------------------------
# wl-08-08-2024, Thu: adjust molecular formula' exact mass
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
        adjusted mass
    """

    try:
        adj = mass + add_dict[adduct]
    # except Exception:
    except KeyError:
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
        'filename' has 'adduct' column.

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
    adj_f = False     # wl-30-08-2024, Fri: do not adjust mass
    if ("adduct" in df.columns) and (lib_adducts is not None) and adj_f:
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


# -----------------------------------------------------------------------
# wl-22-04-2024, Mon: load reference file for compound annotation
# wl-08-08-2024, Thu: use 'cal_mass' function
# wl-10-09-2024, Tue: remove empy rows and columns
# wl-11-09-2024, Wed: rename 'name' as 'molycular_name' in case 'name'
#   conflicts with data set's peak 'name'.
def read_ref(filename, sep="\t", calc=False, lib_adducts=None):
    """
    Load reference for compound annotation

    Parameters
    ----------
    filename : str
        full path for a text reference file
    sep : str
        separator for 'filename'
    calc : bool
        calculate exact mass or not
    lib_adducts : DataFrame
        adducts library in data frame format for mass adjustment. Only for
        'filename' has 'adduct' column.

    Returns
    -------
    DataFrame
        Reference dataframe with exact mass.

    Notes
    -----
    This function will remove reference empty rows and columns.
    """

    # read file
    df = (
        pd.read_csv(filename, sep=sep, float_precision="round_trip")
        .pipe(_remove_empty)
    )

    # wl-11-09-2024, Wed: change name
    df.columns = df.columns.str.replace("^name$", "molecular_name",
                                        regex=True)

    # calculate exact mass
    if calc or ('exact_mass' not in df.columns):
        df = cal_mass(df, lib_adducts)

    return df


# -------------------------------------------------------------------------
def cal_mz_tol(mass, ppm):
    """
    Calculate mz tolerance.

    Parameters
    ----------
    mass : float
        a mass value.
    ppm : float
        ppm value.

    Returns
    -------
    min_tol : float
        Minimal tolerance.
    max_tol : float
        Maxmal tolerance.
    """

    min_tol = mass - (mass * 0.000001 * ppm)
    max_tol = mass + (mass * 0.000001 * ppm)
    return min_tol, max_tol


# -------------------------------------------------------------------------
# wl-24-12-2023, Sun: get library in data frame format
def read_lib(filename, ion_mode=None, sep="\t"):
    """
    Read library file.

    Parameters
    ----------
    filename : str
        library file.
    ion_mode : str
        a string for ion mode, "pos" or "neg".
    sep : str
        file seperater, `\t` or `,`.


    Returns
    -------
    DataFrame
        a library data frame.
    """

    lib_df = pd.read_csv(filename, sep=sep, float_precision="round_trip")

    if "ion_mode" in lib_df:
        idx = (lib_df["ion_mode"] == ion_mode)
        if idx.sum() > 0:
            lib_df = lib_df[idx]
        lib_df = lib_df.drop("ion_mode", axis=1)

    return lib_df


# -------------------------------------------------------------------------
# wl-20-05-2024, Mon: get correlation group and size
def corr_grp_size(corr):
    """
    Get correlation group and size.

    Parameters
    ----------
    corr : DataFrame
        A long-format correlation table. The front two columns
        names must be 'name_a' and 'name_b'. Other columns could be
        correlation coefficient, p-values and any other values.

    Returns
    -------
    DataFrame
        a data frame with three columns, "name", "cor_grp_size" and
        "cor_grp".
    """
    # get correlated groups/clusters
    cor_nam = corr['name_a'].to_list()
    cor_nam.extend(corr['name_b'].to_list())
    cor_nam = list(set(cor_nam))
    cor_grp = [corr_grp(x, corr) for x in cor_nam]
    # cor_grp_dict = {x: mt.corr_grp(x, corr) for x in cor_nam}
    cor_len = [len(x) for x in cor_grp]
    cor_str = ['::'.join(x) for x in cor_grp]
    # merge into a data frame
    cor_df = pd.DataFrame(list(zip(cor_nam, cor_len, cor_str)),
                          columns=['name', 'cor_grp_size', 'cor_grp'])
    cor_df = cor_df.sort_values('cor_grp_size', ignore_index=True,
                                ascending=False)
    return cor_df


# -----------------------------------------------------------------------
# wl-01-05-2024, Wed: get correlation group
def corr_grp(x, corr):
    """
    Get correlated group.

    'x' will mtched in the first two columns of 'corr'.

    Parameters
    ----------
    x : str
        A string for match
    corr : DataFrame
        A long-format correlation table. The front two columns
        names must be 'name_a' and 'name_b'. Other columns could be
        correlation coefficient, p-values and any other values.

    Returns
    -------
    list
        a list consisting matched strings
    """

    ida = corr['name_a'] == x
    a = corr['name_b'][ida].to_list()

    idb = corr['name_b'] == x
    b = corr['name_a'][idb].to_list()

    a.extend(b)

    return a


# -------------------------------------------------------------------------
# wl-04-12-2023, Mon: get correlation coefficients, p-values and rt
# differences for compound annotation.
# Note:
#  - not feasible to return un-filtered results for large data set (>2000)
def comp_corr_rt(df, thres_rt=5.0, thres_corr=0.7, thres_pval=0.05,
                 method="pearson", positive=True):
    """
    Get correlation coefficients, p-values and rt differences for compound
    annotation.

    Parameters
    ----------
    df : DataFrame
        A pandas data frame of peak table. It must have "name", "mz" and
        "rt" columns.
    thres_rt : float
        Threshold for retension time.
    thres_corr : float
        Threshold for correlation coefficients
    thres_pval : float
        Threshold for correlation p-values.
    method : str
        Correlation methods, either "pearson" or "spearman".
    positive : bool
        Use positive correlation or not.

    Returns
    -------
    DataFrame
        A table with differences of retension time, correlation
        coeffocients, correlation p-values.
    """
    # get data for correlation analysis
    mat = df.drop(['name', 'mz', 'rt', 'intensity'], axis=1)

    mat = mat.T                      # transpose
    mat.columns = df["name"]         # change columns' names

    # calculate correlation coefficient and p-values
    corr, pval = df_corr_pval(mat, method=method)
    # corr.isnull().sum()    # check nan
    # pval.isnull().sum()    # check nan

    # filter corr and pval
    if positive:
        corr[corr <= thres_corr] = np.nan
    else:
        corr[abs(corr) <= thres_corr] = np.nan

    pval[pval >= thres_pval] = np.nan

    # convert short format to long format and remove NaNs
    corr = df_short2long(corr)
    corr.rename(columns={'var': 'r_value'}, inplace=True)
    pval = df_short2long(pval)
    pval.rename(columns={'var': 'p_value'}, inplace=True)

    # merge (corr and pval's row number may be different so cannot use
    # pd.concat)
    tab = corr.merge(pval, on=['com1', 'com2'], how='inner')
    del corr, pval     # release memory

    if thres_rt is not None:               # get rt diff
        tmp = df[['name', 'rt']]
        diff = abs(df_diff(tmp))
        diff[diff > thres_rt] = np.nan     # filter rt
        diff = df_short2long(diff)
        diff = diff.rename(columns={'var': 'rt_diff'}).round({'rt_diff': 2})
        # merge corr and pval
        tab = tab.merge(diff, on=['com1', 'com2'], how='inner')
        del tmp, diff     # release memory

    tab = (
        tab
        .rename(columns={"com1": "name_a", "com2": "name_b"})
        .round({'r_value': 2})
    )

    return tab


# -------------------------------------------------------------------------
# wl-28-07-2022, Thu: calculate matrix's correlation and p-values
#   This method calls pandas.DataFrame.corr() twice.
# wl-27-09-2022, Tue: get p-values from https://bit.ly/3frFFUV
# wl-05-12-2023, Tue: fix a mis-understanding of sample size (nData)
# wl-06-12-2023, Wed: 'spearman' is extremely slow. Use rank's 'pearson' as
#  the alternative (ultimately doing the same calculation). For details, see
#  https://bit.ly/4a9y1X2
def df_corr_pval(df, method="pearson", min_periods=4):
    """
    Calculate matrix's correlation and p-values.

    This function calls pandas.DataFrame.corr().

    Parameters
    ----------
    df : DataFRame
        a symmetric data frame.
    method : {'pearson', 'spearman'}
        Method of correlation:
        * pearson : standard correlation coefficient
        * spearman : Spearman rank correlation
    min_periods : int
        Minimum number of observations required per pair of columns
        to have a valid result.

    Returns
    -------
    corr : DataFrame
        correlation matrix
    pval : DataFrame
        p-value matrix

    Examples
    --------
    >>> n = 10        # sample size
    >>> m = 20        # feature size
    >>> df = pd.DataFrame(np.random.random((n, m)))
    >>> df.columns = ['col{}'.format(x) for x in range(m)]
    >>> co, pv = df_corr_pval(df)
    """
    def corr_pval_two_side(cc, nData):
        # We will divide by 0 if correlation is exactly 1, but that is no
        # problem. We would simply set the test statistic to be infinity if
        # it evaluates to NAN
        with np.errstate(divide='ignore'):
            t = -np.abs(cc) * np.sqrt((nData - 2) / (1 - cc**2))
            t[t == np.nan] = np.inf
            # multiply by two to get two-sided p-value
            return scipy.stats.t.cdf(t, nData - 2) * 2

    # get correlation. Very fast for 'pearson'.
    if False:
        corr = df.corr(method=method, min_periods=min_periods)
    else:
        if method == "pearson":
            corr = df.corr(method="pearson", min_periods=min_periods)
        elif method == "spearman":  # 06-12-2023, Wed: fast than 'spearman'
            corr = df.rank().corr(method="pearson", min_periods=min_periods)
        else:
            raise ValueError("Method must be either 'pearson' or 'spearman'.")

    flag = False
    if flag:    # call df.corr again
        if method == "pearson":
            meth_corr = scipy.stats.pearsonr
        elif method == "spearman":
            meth_corr = scipy.stats.spearmanr
        else:
            raise ValueError("Method must be either 'pearson' or 'spearman'.")
        # get p-values
        pval = df.corr(method=lambda x, y: meth_corr(x, y)[1],
                       min_periods=min_periods) - np.eye(len(df.columns))
    else:       # use local function
        # sample size is row of df, not col of df
        pval = corr_pval_two_side(corr, df.shape[0])
        # pval = corr_to_pval(corr, df.shape[0])
        pval = pd.DataFrame(pval)
        # set dimension names as 'corr'
        pval.index = corr.index
        pval.columns = corr.columns

    return corr, pval


# -------------------------------------------------------------------------
# wl-04-12-2023, Mon: Convert short to long format and remove NAs
# Note that this function will remove NAs.
def df_short2long(df):
    """
    Convert a symmetric matrix to a pair-wise matrix.

    This function convert so-called short format matrix to long format
    matrix. Also the missing values will be removed.

    Parameters
    ----------
    df : DataFRame
        a symmetric data frame.

    Returns
    -------
    DataFrame
        a data frame.
    """

    # reset columns and index names
    df = df.rename_axis(None).rename_axis(None, axis=1)
    # df.index.name = None

    # reshape data frame
    long_df = df.stack().reset_index()
    long_df.columns = ['com1', 'com2', 'var']

    # Exclude the diagonal and duplicate entries
    if True:
        long_df = long_df[long_df['com1'] < long_df['com2']]
    else:
        # create a mask to identify rows with duplicate features
        # See https://bit.ly/3Ooei9W for details.
        idx = (
            (long_df[['com1', 'com2']].apply(frozenset, axis=1).duplicated()) | \
            (long_df['com1'] == long_df['com2'])
        )
        # update
        long_df = long_df[~idx]

    # reset row names
    long_df.reset_index(drop=True, inplace=True)

    return long_df


# -------------------------------------------------------------------------
# wl-25-07-2022, Mon: calculate pairwise difference
# See https://bit.ly/3outZSs for details.
def df_diff(df):
    """
    Calculate pairwise difference of a data frame.

    Parameters
    ----------
    df : DataFrame
        a data frame.

    Returns
    -------
    DataFrame
        a data frome with pair-wise differences.

    Examples
    --------
    >>> tmp = {'Country':['GB','JP','US'],'Values':[20.2,-10.5,5.7]}
    >>> tmp = pd.DataFrame(tmp)
    >>> df_diff(tmp)
    """

    # use apply to get symmetric difference matrix
    arr = df.iloc[:, 1].apply(lambda x: df.iloc[:, 1] - x)
    # arr = abs(arr)

    # change row ad column names
    arr.index = list(df.iloc[:, 0])
    arr.columns = list(df.iloc[:, 0])

    return arr


# ------------------------------------------------------------------------
# wl-29-12-2023, Fri: convert 2-columns data frame to dict
def df2dict(df):
    """
    Convert 2-columns DataFrame to dict.

    Parameters
    ----------
    df : DataFrme
        a two columns data frame.

    Returns
    -------
    dict
        a dict.

    Notes
    -----
    This function is used to speedy query.
    """

    res = zip(df.iloc[:, 0], df.iloc[:, 1])
    res = list(res)
    res = dict(res)
    return res


# -------------------------------------------------------------------------
# wl-18-05-2024, Sat: flat column names.
# use 'pipe' inside a chain
def flatten_cols(df):
    """
    Flat column names.

    Parameters
    ----------
    df : DataFrame
        a data frame.

    Returns
    -------
    DataFrame
        a data frame with falltern column names.
    """

    df.columns = ["_".join(x) for x in df.columns.to_flat_index()]
    return df


# -------------------------------------------------------------------------
# wl-27-12-2023, Wed: Remove empty cell and flatten list
def flatten_list(list):
    """
    Remove empty cell and flatten list.

    Parameters
    ----------
    list : list
        a nested list with empty elements.

    Returns
    -------
    list
        a flattern list.
    """

    # remove empty item
    list = [x for x in list if x]
    # flatten list
    res = [item for lt in list for item in lt]
    return res


# --------------------------------------------------------------------------
# wl-21-09-2022, Wed: Read file consisting of peak list and data matrix.
# wl-02-09-2024, Mon: add 'dat' format for Galaxy data extension
def read_peak(fn, cols=[1, 2, 3, 4], sep="\t", median_intensity=True):
    """
    Read metabolite data.

    The file must have peak-list and intensity data and must be one of file
    formats: xls, xlsx, txt, csv and tsv.

    Parameters
    ----------
    fn : str
        file name.
    cols : list
        a list indicating column index of 'name', 'mz', 'rt' and start of
        intensity
    sep : str
        file separator for txt, csv and tsv file. `\t` or `,`.
    median_intensity : bool
        use median or mean for average of intensity.

    Returns
    -------
    DataFrame
        a data frame with the first 4 columns as name, mz, rt and intensity
    """

    ext = os.path.splitext(fn)[1][1:]
    if ext in ['xls', 'xlsx']:
        data = pd.read_excel(fn, header=0)
    elif ext in ['txt', 'csv', 'tsv', 'dat']:
        data = pd.read_table(fn, header=0, sep=sep)
    else:
        raise ValueError("Data must be: 'xls', 'xlsx', 'txt', 'csv', 'tsv' or dat.")

    # data = pd.read_table(fn, header=0, sep=sep)

    # get python index
    cols = [x - 1 for x in cols]
    # cols = list(map(lambda x: x - 1, cols))

    # get peak list
    peak = data.iloc[:, cols[:3]]

    # get intensity
    mat = data.iloc[:, cols[-1]:]
    if median_intensity:
        intensity = mat.median(axis=1, skipna=True)
    else:
        intensity = mat.mean(axis=1, skipna=True)

    # column bind ('cbind' in R)
    data = pd.concat([peak, intensity, mat], axis=1, ignore_index=False)

    data.rename(columns={data.columns[0]: 'name',
                         data.columns[1]: 'mz',
                         data.columns[2]: 'rt',
                         data.columns[3]: 'intensity'},
                inplace=True)
    data['name'] = data['name'].astype(str)

    # replace 0 with na for the future correlation analysis
    data.replace(0, np.nan, inplace=True)

    return data


# -------------------------------------------------------------------------
# wl-02-08-2022, Tue: Measure running time.
# Matlab's tic and toc time measuring. From https://bit.ly/3SuXktQ
def _tic():
    """ Matlab's tic and toc time measuring. """
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


# -------------------------------------------------------------------------
def _toc():
    """ Matlab's tic and toc time measuring. """
    if 'startTime_for_tictoc' in globals():
        elap_time = time.time() - startTime_for_tictoc
        print("Elapsed time: " + str(elap_time) + " seconds.")
    else:
        print("Toc: start time not set")


# -----------------------------------------------------------------------
# wl-10-09-2024, Tue: remove empyty rows and columns
def _remove_empty(df, reset_index=True):
    """
    Drop all rows and columns that are completely null

    Parameters
    ----------
    df : DataFrame
        The pandas DataFrame object.
    reset_index : bool
        Determines if the index is reset.

    Returns
    -------
    DataFrame
        A pandas DataFrame.

    Notes
    -----
    This function is taken from package `janitor`'s `remove_empty`.
    """

    outcome = df.isna()
    outcome = df.loc[~outcome.all(axis=1), ~outcome.all(axis=0)]
    if reset_index:
        return outcome.reset_index(drop=True)
    return outcome
