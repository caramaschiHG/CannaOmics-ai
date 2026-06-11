"""Prediction utilities."""

from pathlib import Path
from typing import Any

import pandas as pd

from .model_registry import load_model


def predict(model: Any, X: pd.DataFrame) -> pd.DataFrame:
    """
    Generate predictions and probabilities for new data.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        Trained model.
    X : pd.DataFrame
        Features to predict on.

    Returns
    -------
    pd.DataFrame
        DataFrame with predictions and (if available) probabilities.
    """
    results = pd.DataFrame(index=X.index)
    results["prediction"] = model.predict(X)

    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X)
            # Add probability columns for each class
            for i, cls in enumerate(model.classes_):
                results[f"probability_{cls}"] = proba[:, i]
        except Exception:
            pass

    return results


def predict_from_registry(model_dir: Path, X: pd.DataFrame) -> pd.DataFrame:
    """
    Load a model from the registry and generate predictions.

    Parameters
    ----------
    model_dir : Path
        Directory containing the saved model.
    X : pd.DataFrame
        Features to predict on.

    Returns
    -------
    pd.DataFrame
        Predictions.
    """
    model, _ = load_model(model_dir)
    return predict(model, X)
