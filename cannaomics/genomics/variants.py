"""Variant loading and manipulation utilities."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class VariantInfo:
    """Information about a specific genomic variant."""

    variant_id: str
    chromosome: str
    position: int
    ref: str
    alt: str
    variant_type: str = "SNP"
    nearest_gene: str | None = None
    distance_to_gene: int | None = None
    within_gene: bool = False
    effect: str | None = None
    source_dataset: str | None = None


def load_variant_matrix(path: Path) -> pd.DataFrame:
    """
    Load a variant matrix from a CSV or Parquet file.

    The matrix is expected to have samples as rows and variants as columns.
    The first column should be 'sample_id'.

    Parameters
    ----------
    path : Path
        Path to the variant matrix file.

    Returns
    -------
    pd.DataFrame
        The loaded variant matrix.
    """
    path_str = str(path)
    if path_str.endswith(".csv"):
        df = pd.read_csv(path)
    elif path_str.endswith(".parquet"):
        df = pd.read_parquet(path)
    else:
        raise ValueError(
            f"Unsupported file format: {path.suffix}. Use .csv or .parquet"
        )

    if "sample_id" not in df.columns:
        raise ValueError("Variant matrix must contain a 'sample_id' column.")

    return df


def filter_variants(
    df: pd.DataFrame, min_maf: float = 0.05, max_missing: float = 0.1
) -> pd.DataFrame:
    """
    Filter variants based on Minor Allele Frequency (MAF) and missingness.

    Parameters
    ----------
    df : pd.DataFrame
        Variant matrix (0/1/2 encoding assumed, or floats).
    min_maf : float, optional
        Minimum minor allele frequency, default 0.05.
    max_missing : float, optional
        Maximum proportion of missing values allowed, default 0.1.

    Returns
    -------
    pd.DataFrame
        Filtered variant matrix.
    """
    # Assuming sample_id is the index or first col.
    var_cols = [c for c in df.columns if c != "sample_id"]

    # Filter by missingness
    missing_rates = df[var_cols].isna().mean()
    keep_cols_missing = missing_rates[missing_rates <= max_missing].index

    # Very basic MAF filtering (assuming 0, 1, 2 encoding)
    # Calculate allele frequency (sum / (2 * n_non_missing))
    # This is a simplification for the MVP.
    af = df[keep_cols_missing].sum() / (2 * df[keep_cols_missing].notna().sum())
    maf = af.apply(lambda x: min(x, 1 - x))

    keep_cols_maf = maf[maf >= min_maf].index

    final_cols = (
        ["sample_id", *list(keep_cols_maf)]
        if "sample_id" in df.columns
        else list(keep_cols_maf)
    )
    return df[final_cols]


def summarize_variants(df: pd.DataFrame) -> dict[str, Any]:
    """
    Compute basic statistics for a variant matrix.

    Parameters
    ----------
    df : pd.DataFrame
        The variant matrix.

    Returns
    -------
    dict
        Dictionary of summary statistics.
    """
    var_cols = [c for c in df.columns if c != "sample_id"]
    n_samples = len(df)
    n_variants = len(var_cols)

    if n_variants == 0:
        return {"n_samples": n_samples, "n_variants": 0}

    missing_rate = df[var_cols].isna().mean().mean()

    return {
        "n_samples": n_samples,
        "n_variants": n_variants,
        "average_missing_rate": missing_rate,
    }
