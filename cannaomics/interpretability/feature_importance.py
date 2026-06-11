"""Feature importance calculation utilities."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance


def compute_permutation_importance(
    model: Any,
    X: pd.DataFrame,
    y: pd.Series,
    n_repeats: int = 10,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Compute permutation importance for model features.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        Trained model.
    X : pd.DataFrame
        Features matrix.
    y : pd.Series
        Target vector.
    n_repeats : int, optional
        Number of times to permute a feature.
    random_state : int, optional
        Random seed.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'feature', 'importance_mean', 'importance_std', 'rank'.
    """
    result = permutation_importance(
        model, X, y, n_repeats=n_repeats, random_state=random_state, n_jobs=-1
    )

    importance_df = pd.DataFrame(
        {
            "feature": X.columns,
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
        }
    )

    # Sort and rank
    importance_df = importance_df.sort_values(
        "importance_mean", ascending=False
    ).reset_index(drop=True)
    importance_df["rank"] = importance_df.index + 1

    return importance_df


def get_model_importance(model: Any, feature_names: list) -> pd.DataFrame:
    """
    Extract native model feature importance (if available).

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        Trained model.
    feature_names : list
        List of feature names.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'feature' and 'importance' columns.
    """
    importances = None

    # Random Forest / XGBoost
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    # Linear models
    elif hasattr(model, "coef_"):
        # For multi-class, take the max absolute coefficient across classes
        coefs = model.coef_
        if len(coefs.shape) > 1 and coefs.shape[0] > 1:
            importances = np.max(np.abs(coefs), axis=0)
        else:
            importances = np.abs(coefs[0])

    if importances is None:
        # Fallback if model has no native importance
        importances = np.zeros(len(feature_names))

    df = pd.DataFrame({"feature": feature_names, "model_importance": importances})

    return df.sort_values("model_importance", ascending=False).reset_index(drop=True)


def compute_stable_importance(
    model: Any, X: pd.DataFrame, y: pd.Series, n_splits: int = 5
) -> pd.DataFrame:
    """Compute average importance across CV folds.

    Placeholder for MVP - currently delegates to permutation importance on
    the full dataset; will be extended to aggregate per-fold importances.
    """
    _ = n_splits  # Reserved for real CV-based implementation.
    return compute_permutation_importance(model, X, y)
