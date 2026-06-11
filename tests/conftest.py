"""Pytest configuration and shared fixtures."""


import pandas as pd
import pytest


@pytest.fixture
def sample_chemical_df():
    """Provides a synthetic chemical profile dataframe."""
    return pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "THC": [15.0, 0.5, 8.0, 0.0],
            "CBD": [0.1, 12.0, 9.0, 0.0],
            "beta_myrcene": [1.2, 0.5, 0.8, 0.1],
        }
    )


@pytest.fixture
def sample_variant_df():
    """Provides a synthetic variant matrix dataframe."""
    return pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "CsTPS1_exp_1": [10.5, 2.1, 8.3, 0.5],
            "THCAS_region_snp_01": [2, 0, 1, 0],
            "random_snp": [0, 1, 0, 1],
        }
    )
