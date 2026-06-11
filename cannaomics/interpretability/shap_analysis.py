"""SHAP analysis with graceful fallback."""

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from ..utils.logging import get_logger

logger = get_logger("shap_analysis")

try:
    import shap

    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    logger.warning("SHAP is not installed. SHAP analysis will be skipped.")


@dataclass
class ShapResult:
    """Results from SHAP analysis."""

    shap_values: np.ndarray
    expected_value: Any
    feature_names: list[str]


def compute_shap_values(
    model: Any, X: pd.DataFrame, max_samples: int = 100
) -> ShapResult | None:
    """
    Compute SHAP values for a model.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        Trained model.
    X : pd.DataFrame
        Features matrix.
    max_samples : int, optional
        Maximum number of samples to use for explaining (performance optimization).

    Returns
    -------
    Optional[ShapResult]
        SHAP results, or None if SHAP is not available or fails.
    """
    if not SHAP_AVAILABLE:
        return None

    try:
        # Sample if dataset is large
        if len(X) > max_samples:
            X_sample = shap.sample(X, max_samples)
        else:
            X_sample = X

        # Try TreeExplainer for forests/trees
        if type(model).__name__ in [
            "RandomForestClassifier",
            "XGBClassifier",
            "RandomForestRegressor",
        ]:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_sample)
            expected_value = explainer.expected_value

        # Try LinearExplainer for linear models
        elif type(model).__name__ in [
            "LogisticRegression",
            "SGDClassifier",
            "Ridge",
            "Lasso",
        ]:
            explainer = shap.LinearExplainer(model, X_sample)
            shap_values = explainer.shap_values(X_sample)
            expected_value = explainer.expected_value

        # Fallback to general Explainer
        else:
            explainer = shap.Explainer(model.predict, X_sample)
            shap_values_obj = explainer(X_sample)
            shap_values = shap_values_obj.values
            expected_value = shap_values_obj.base_values

        return ShapResult(
            shap_values=np.array(shap_values),
            expected_value=expected_value,
            feature_names=list(X.columns),
        )

    except Exception as e:
        logger.error(f"SHAP computation failed: {e}")
        return None


def get_top_shap_features(shap_result: ShapResult, n: int = 20) -> pd.DataFrame:
    """
    Extract top features by mean absolute SHAP value.

    Parameters
    ----------
    shap_result : ShapResult
        Result from compute_shap_values.
    n : int, optional
        Number of top features to return.

    Returns
    -------
    pd.DataFrame
        DataFrame with feature names and mean absolute SHAP values.
    """
    if shap_result is None or shap_result.shap_values is None:
        return pd.DataFrame()

    vals = shap_result.shap_values

    # Handle multi-class / list of arrays
    if isinstance(vals, list):
        # Average across classes
        vals = np.mean(np.abs(np.array(vals)), axis=0)
    elif len(vals.shape) == 3:
        # Array shape (samples, features, classes)
        vals = np.mean(np.abs(vals), axis=2)
    else:
        vals = np.abs(vals)

    mean_abs_shap = np.mean(vals, axis=0)

    df = pd.DataFrame(
        {"feature": shap_result.feature_names, "mean_abs_shap": mean_abs_shap}
    )

    return (
        df.sort_values("mean_abs_shap", ascending=False).head(n).reset_index(drop=True)
    )
