"""Chemotype classification utilities."""

from enum import Enum

import pandas as pd


class ChemotypeLabel(Enum):
    """Enumeration of standard Cannabis chemotypes."""

    THC_DOMINANT = "THC-dominant"
    CBD_DOMINANT = "CBD-dominant"
    BALANCED = "Balanced"
    OTHER = "Other"


def classify_chemotype(thc: float, cbd: float, method: str = "ratio") -> ChemotypeLabel:
    """
    Classify a sample into a primary cannabinoid chemotype.

    Parameters
    ----------
    thc : float
        THC concentration (typically THC + THCA, but depends on input data).
    cbd : float
        CBD concentration (typically CBD + CBDA).
    method : str, optional
        Classification method, currently supports 'ratio'.

    Returns
    -------
    ChemotypeLabel
        The assigned chemotype label.
    """
    if pd.isna(thc) or pd.isna(cbd):
        return ChemotypeLabel.OTHER

    if thc <= 0 and cbd <= 0:
        return ChemotypeLabel.OTHER

    # Avoid division by zero
    if cbd == 0:
        return ChemotypeLabel.THC_DOMINANT if thc > 0 else ChemotypeLabel.OTHER
    if thc == 0:
        return ChemotypeLabel.CBD_DOMINANT if cbd > 0 else ChemotypeLabel.OTHER

    ratio = thc / cbd

    if ratio > 5.0:
        return ChemotypeLabel.THC_DOMINANT
    elif ratio < 0.2:
        return ChemotypeLabel.CBD_DOMINANT
    else:
        return ChemotypeLabel.BALANCED


def classify_high_low(
    values: pd.Series, method: str = "median", threshold: float | None = None
) -> pd.Series:
    """
    Classify a continuous variable into high/low categories.

    Parameters
    ----------
    values : pd.Series
        Numeric series to classify.
    method : str, optional
        'median', 'quantile', or 'absolute'.
    threshold : float, optional
        Value to use for absolute threshold or quantile.

    Returns
    -------
    pd.Series
        Series containing 'high' or 'low' string labels.
    """
    # Drop NAs for threshold calculation
    clean_values = values.dropna()

    if len(clean_values) == 0:
        return pd.Series(index=values.index, dtype="object")

    if method == "median":
        thresh_val = clean_values.median()
    elif method == "quantile":
        q = threshold if threshold is not None else 0.75
        thresh_val = clean_values.quantile(q)
    elif method == "absolute":
        if threshold is None:
            raise ValueError("Absolute method requires a threshold value.")
        thresh_val = threshold
    else:
        raise ValueError(f"Unknown threshold method: {method}")

    # Create categorical series
    result = pd.Series("low", index=values.index)
    result.loc[values > thresh_val] = "high"
    result.loc[values.isna()] = pd.NA

    return result


def classify_samples(chemical_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add chemotype classifications to a chemical profiles DataFrame.

    Parameters
    ----------
    chemical_df : pd.DataFrame
        DataFrame with normalized compound columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'chemotype' column.
    """
    df = chemical_df.copy()

    if "THC" in df.columns and "CBD" in df.columns:
        df["chemotype"] = df.apply(
            lambda row: classify_chemotype(row.get("THC", 0), row.get("CBD", 0)).value,
            axis=1,
        )
    return df
