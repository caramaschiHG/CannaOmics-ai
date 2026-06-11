"""Tests for chemistry module."""

import pandas as pd

from cannaomics.chemistry.chemotype import (
    ChemotypeLabel,
    classify_chemotype,
    classify_high_low,
)
from cannaomics.chemistry.normalize_compounds import (
    normalize_columns,
    normalize_compound_name,
)


def test_normalize_compound_name():
    assert normalize_compound_name("b-myrcene") == "beta_myrcene"
    assert normalize_compound_name("  δ9-THC  ") == "THC"
    assert normalize_compound_name("unknown_compound") == "unknown_compound"


def test_normalize_columns():
    df = pd.DataFrame({"sample_id": ["S1"], "d-limonene": [1.0], "CBDA": [2.0]})
    norm_df = normalize_columns(df)
    assert list(norm_df.columns) == ["sample_id", "limonene", "CBDA"]


def test_classify_chemotype():
    assert classify_chemotype(20.0, 0.1) == ChemotypeLabel.THC_DOMINANT
    assert classify_chemotype(0.5, 15.0) == ChemotypeLabel.CBD_DOMINANT
    assert classify_chemotype(8.0, 9.0) == ChemotypeLabel.BALANCED
    assert classify_chemotype(0.0, 0.0) == ChemotypeLabel.OTHER


def test_classify_high_low():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    res = classify_high_low(s, method="median")
    assert list(res) == ["low", "low", "low", "high", "high"]
