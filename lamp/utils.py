import time


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
