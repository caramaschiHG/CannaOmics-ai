"""Tests for pipeline integration."""

import pandas as pd

from cannaomics.features.build_features import build_feature_matrix


def test_build_feature_matrix():
    chem = pd.DataFrame({"sample_id": ["S1", "S2"], "THC": [10.0, 20.0]}).set_index(
        "sample_id"
    )
    var = pd.DataFrame({"sample_id": ["S1", "S2"], "snp1": [0, 1]}).set_index(
        "sample_id"
    )

    X, y = build_feature_matrix(var, chem, "THC")
    assert len(X) == 2
    assert len(y) == 2
