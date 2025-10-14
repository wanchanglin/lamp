import scipy
import numpy as np
import pandas as pd


# -------------------------------------------------------------------------
# wl-04-12-2023, Mon: get correlation coefficients, p-values and rt
# differences for compound annotation.
# wl-15-11-2024, Fri: minor changes
# wl-29-07-2025, Sun: call updated 'df_corr_pval'
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
        Threshold for retention time.
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
        A table with differences of retention time, correlation
        coefficients, correlation p-values.
    """

    # get data for correlation analysis
    mat = df.drop(['name', 'mz', 'rt'], axis=1)
    mat = mat.T                      # transpose
    mat.columns = df["name"]         # change columns' names

    # calculate correlation coefficient and p-values
    corr, pval = df_corr_pval(mat, thres_corr=thres_corr,
                              thres_pval=thres_pval, method=method,
                              positive=positive)
    # corr.isnull().sum()    # check nan
    # pval.isnull().sum()    # check nan

    # get rt difference and filter it
    tmp = df[['name', 'rt']]
    diff = abs(df_diff(tmp))
    diff[diff > thres_rt] = np.nan

    # combine three conditions
    ind = corr.notnull() & pval.notnull() & diff.notnull()

    # update
    corr = corr[ind]
    pval = pval[ind]
    diff = diff[ind]

    # convert to long format
    corr = df_short2long(corr).rename(columns={'var': 'r_value'})
    pval = df_short2long(pval).rename(columns={'var': 'p_value'})
    diff = df_short2long(diff).rename(columns={'var': 'rt_diff'})

    # merge
    tab = (
        corr
        .merge(pval, on=['com1', 'com2'], how='inner')
        .merge(diff, on=['com1', 'com2'], how='inner')
        .rename(columns={"com1": "name_a", "com2": "name_b"})
        .round({'r_value': 2})
        .round({'rt_diff': 2})
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
# wl-18-11-2024, Mon: convert float64 to float32
# wl-29-07-2025, Sun: filter corr and pval to reduce memory consumption.
#   (I doubt. Maybe sparse df can be. 02-07-2025, Wed)
def df_corr_pval(df, thres_corr=0.7, thres_pval=0.05, method="pearson",
                 positive=True, min_periods=4):
    """
    Calculate matrix's correlation and p-values.

    This function calls pandas.DataFrame.corr().

    Parameters
    ----------
    df : DataFrame
        A symmetric data frame.
    thres_corr : float
        Threshold for correlation coefficients
    thres_pval : float
        Threshold for correlation p-values.
    method : {'pearson', 'spearman'}
        Method of correlation:
        * pearson : standard correlation coefficient
        * spearman : Spearman rank correlation
    positive : bool
        Use positive correlation or not.
    min_periods : int
        Minimum number of observations required per pair of columns
        to have a valid result.

    Returns
    -------
    corr : DataFrame
        Correlation matrix
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
    def corr_pval_two_side(cc, sample_size):
        # We will divide by 0 if correlation is exactly 1, but that is no
        # problem. We would simply set the test statistic to be infinity if
        # it evaluates to NAN
        with np.errstate(divide='ignore'):
            t = -np.abs(cc) * np.sqrt((sample_size - 2) / (1 - cc**2))
            t[t == np.nan] = np.inf
            t = t.astype('float32')
            # multiply by two to get two-sided p-value
            res = scipy.stats.t.cdf(t, sample_size - 2) * 2
            return res

    df = df_64_32(df)

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

    corr = corr.astype('float32')

    # filter corr
    if positive:
        corr[corr <= thres_corr] = np.nan
    else:
        corr[abs(corr) <= thres_corr] = np.nan

    # get p-value by local function
    # sample size is row of df, not col of df
    pval = corr_pval_two_side(corr, df.shape[0])
    pval = pd.DataFrame(pval)
    # set dimension names as 'corr'
    pval.index = corr.index
    pval.columns = corr.columns

    # filter pval
    pval[pval >= thres_pval] = np.nan
    pval = pval.astype('float32')

    return corr, pval


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
        A data frame with three columns, "name", "cor_grp_size" and
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

    'x' will match in the first two columns of 'corr'.

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
        A list consisting matched strings.
    """

    ida = corr['name_a'] == x
    a = corr['name_b'][ida].to_list()

    idb = corr['name_b'] == x
    b = corr['name_a'][idb].to_list()

    a.extend(b)

    return a


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
        A symmetric data frame.

    Returns
    -------
    DataFrame
        A data frame.
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
# wl-18-11-2024, Mon: convert float64 to float32
def df_diff(df):
    """
    Calculate pairwise difference of a data frame.

    Parameters
    ----------
    df : DataFrame
        A data frame.

    Returns
    -------
    DataFrame
        A data from with pair-wise differences.

    Examples
    --------
    >>> tmp = {'Country':['GB','JP','US'],'Values':[20.2,-10.5,5.7]}
    >>> tmp = pd.DataFrame(tmp)
    >>> df_diff(tmp)
    """

    df = df_64_32(df)

    # use apply to get symmetric difference matrix
    dif = df.iloc[:, 1].apply(lambda x: df.iloc[:, 1] - x)
    # dif = abs(dif)

    # change row ad column names
    dif.index = list(df.iloc[:, 0])
    dif.columns = list(df.iloc[:, 0])

    return dif


# -------------------------------------------------------------------------
# wl-18-11-2024, Mon: convert float64 to float32
def df_64_32(df):
    """
    Convert Pandas dataframe's float64 columns to float32.

    Parameters
    ----------
    df : DataFrame
        A data frame with float64 columns.

    Returns
    -------
    DataFrame
        A converted data frame.

    Notes
    -----
    This function is used to large dataset's correlation analysis.
    """
    # 25-06-2025, Wed: add this line otherwise will change in-place
    df = df.copy()
    df[df.select_dtypes(np.float64).columns] = df.select_dtypes(
        np.float64).astype(np.float32)
    return df
