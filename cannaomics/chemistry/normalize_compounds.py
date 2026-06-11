"""Compound normalization and harmonization utilities."""

import pandas as pd

# Synonym mapping dictionary.
# Maps common variations to our canonical internal representation.
SYNONYM_MAP = {
    # Terpenes
    "b-myrcene": "beta_myrcene",
    "β-myrcene": "beta_myrcene",
    "myrcene": "beta_myrcene",
    "beta-myrcene": "beta_myrcene",
    "d-limonene": "limonene",
    "l-limonene": "limonene",
    "limonene": "limonene",
    "a-pinene": "alpha_pinene",
    "α-pinene": "alpha_pinene",
    "alpha-pinene": "alpha_pinene",
    "pinene": "alpha_pinene",  # Assume alpha unless specified
    "b-pinene": "beta_pinene",
    "β-pinene": "beta_pinene",
    "beta-pinene": "beta_pinene",
    "b-caryophyllene": "beta_caryophyllene",
    "β-caryophyllene": "beta_caryophyllene",
    "beta-caryophyllene": "beta_caryophyllene",
    "caryophyllene": "beta_caryophyllene",
    "a-humulene": "alpha_humulene",
    "α-humulene": "alpha_humulene",
    "alpha-humulene": "alpha_humulene",
    "humulene": "alpha_humulene",
    "terpinolene": "terpinolene",
    "a-terpinolene": "terpinolene",
    "ocimene": "ocimene",
    "b-ocimene": "ocimene",
    "linalool": "linalool",
    # Cannabinoids
    "δ9-thc": "THC",
    "delta-9-thc": "THC",
    "delta9-thc": "THC",
    "d9-thc": "THC",
    "thc": "THC",
    "thca": "THCA",
    "thc-a": "THCA",
    "cbd": "CBD",
    "cbda": "CBDA",
    "cbd-a": "CBDA",
    "cbc": "CBC",
    "cbca": "CBCA",
    "cbg": "CBG",
    "cbga": "CBGA",
    "thcv": "THCV",
    "cbdv": "CBDV",
}


def normalize_compound_name(name: str) -> str:
    """
    Normalize a compound name to its canonical representation.

    Parameters
    ----------
    name : str
        The raw compound name.

    Returns
    -------
    str
        The normalized canonical name.
    """
    # Lowercase and strip whitespace
    clean_name = str(name).lower().strip()
    return SYNONYM_MAP.get(clean_name, clean_name)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the column names of a DataFrame using the synonym map.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with raw column names.

    Returns
    -------
    pd.DataFrame
        DataFrame with normalized column names.
    """
    normalized_df = df.copy()
    new_cols = {col: normalize_compound_name(col) for col in df.columns}
    normalized_df.rename(columns=new_cols, inplace=True)
    return normalized_df


def normalize_values(df: pd.DataFrame, unit: str = "percent") -> pd.DataFrame:
    """
    Ensure values are numeric and handle basic unit conversions if needed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with chemical values.
    unit : str, optional
        Target unit, default 'percent'.

    Returns
    -------
    pd.DataFrame
        DataFrame with clean numeric values.
    """
    normalized_df = df.copy()

    # Basic numeric conversion, forcing errors to NaN
    for col in normalized_df.columns:
        if col != "sample_id":
            normalized_df[col] = pd.to_numeric(normalized_df[col], errors="coerce")

    # Unit normalization logic could be expanded here.
    # For now, we assume values are already correctly scaled.

    return normalized_df
