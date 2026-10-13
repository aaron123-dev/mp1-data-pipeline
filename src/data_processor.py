import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {before} -> {len(df)} rows")
    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    rows_before =  len(df)
    cols_before = len(df.columns)

    if axis == "rows":
        df = df.dropna(axis = 0)
        logger.debug(f"handle_missing: {rows_before} -> {len(df)} rows")
    elif axis == "columns":
        df = df.dropna(axis = 1)
        logger.debug(f"handle_missing: {cols_before} -> {len(df.columns)} columns")
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")
    return df



def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")
    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue

        
        before = len(df)

        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3-q1
            lower = q1- threshold * iqr
            upper = q3 + threshold * iqr
            df = df[(df[col] >= lower) & (df[col] <= upper)]
            logger.debug(f"{col}: method = {method}, threshold = {threshold}, lower = {lower}, upper = {upper}, removed = {before - len(df)}")
        else:
            z = (df[col] - df[col].mean()) / df[col].std()
            df = df[z.abs() <= threshold]
            logger.debug(f"{col}: method={method}, threshold={threshold}, removed={before - len(df)}")

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)

    missing = settings["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis=missing["axis"])

    outliers = settings["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(
            df,
            outliers["columns"],
            outliers["method"],
            outliers["threshold"]
        )
    return df 


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return{
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
        }