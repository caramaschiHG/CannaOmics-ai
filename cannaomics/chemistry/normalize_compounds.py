"""Compound normalization and harmonization utilities."""

from __future__ import annotations

import pandas as pd

# Synonym mapping dictionary.
# Maps common variations to our canonical internal representation.
# Greek-letter variants are normalised inside ``normalize_compound_name`` via
# a translation table, so we only store ASCII forms here.
SYNONYM_MAP: dict[str, str] = {
    # Terpenes
    "b-myrcene": "beta_myrcene",
    "myrcene": "beta_myrcene",
    "beta-myrcene": "beta_myrcene",
    "d-limonene": "limonene",
    "l-limonene": "limonene",
    "limonene": "limonene",
    "a-pinene": "alpha_pinene",
    "alpha-pinene": "alpha_pinene",
    "pinene": "alpha_pinene",  # Assume alpha unless specified
    "b-pinene": "beta_pinene",
    "beta-pinene": "beta_pinene",
    "b-caryophyllene": "beta_caryophyllene",
    "beta-caryophyllene": "beta_caryophyllene",
    "caryophyllene": "beta_caryophyllene",
    "a-humulene": "alpha_humulene",
    "alpha-humulene": "alpha_humulene",
    "humulene": "alpha_humulene",
    "terpinolene": "terpinolene",
    "a-terpinolene": "terpinolene",
    "ocimene": "ocimene",
    "b-ocimene": "ocimene",
    "linalool": "linalool",
    # Cannabinoids
    "d9-thc": "THC",
    "delta-9-thc": "THC",
    "delta9-thc": "THC",
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

# Greek letters and unicode prefixes commonly used in chemical nomenclature.
# These are translated to ASCII equivalents before lookup so callers can pass
# either form transparently.
_GREEK_TO_ASCII = str.maketrans(
    {
        "\u03b1": "a",  # GREEK SMALL LETTER ALPHA
        "\u03b2": "b",  # GREEK SMALL LETTER BETA
        "\u03b3": "g",  # GREEK SMALL LETTER GAMMA
        "\u03b4": "d",  # GREEK SMALL LETTER DELTA
    }
)


def _to_ascii(name: str) -> str:
    """Translate Greek letters in *name* to ASCII equivalents."""
    return name.translate(_GREEK_TO_ASCII)


def normalize_compound_name(name: str) -> str:
    """Normalize a compound name to its canonical representation.

    Parameters
    ----------
    name : str
        The raw compound name (may contain Greek letters, whitespace, casing).

    Returns
    -------
    str
        The normalized canonical name, or the cleaned input if unknown.
    """
    clean_name = _to_ascii(str(name)).lower().strip()
    return SYNONYM_MAP.get(clean_name, clean_name)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the column names of a DataFrame using the synonym map.

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
    """Ensure values are numeric and handle basic unit conversions if needed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with chemical values.
    unit : str, optional
        Target unit, default ``"percent"``. Reserved for future unit
        conversion logic.

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
    _ = unit  # Reserved for future use; explicit acknowledgement.

    return normalized_df
