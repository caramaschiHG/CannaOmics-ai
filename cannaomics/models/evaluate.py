"""Model evaluation metrics and reporting."""

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from rich.table import Table
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)


@dataclass
class EvalResult:
    """Comprehensive evaluation metrics for a single model."""

    accuracy: float
    balanced_accuracy: float
    f1: float
    roc_auc: float | None
    pr_auc: float | None
    confusion_matrix: np.ndarray
    classification_report: str

    def to_dict(self) -> dict[str, float]:
        """Return scalar metrics as dictionary."""
        d = {
            "accuracy": self.accuracy,
            "balanced_accuracy": self.balanced_accuracy,
            "f1": self.f1,
        }
        if self.roc_auc is not None:
            d["roc_auc"] = self.roc_auc
        if self.pr_auc is not None:
            d["pr_auc"] = self.pr_auc
        return d


def evaluate_model(model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> EvalResult:
    """
    Evaluate a trained model on a test set.

    Parameters
    ----------
    model : BaseEstimator
        Trained sklearn-compatible model.
    X_test : pd.DataFrame
        Test features.
    y_test : pd.Series
        Test true labels.

    Returns
    -------
    EvalResult
        Dataclass containing all metrics.
    """
    y_pred = model.predict(X_test)

    # Try to get probabilities for AUC metrics
    y_proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X_test)
            y_proba = proba[:, 1] if proba.shape[1] == 2 else proba
        except Exception:
            pass

    # Compute metrics
    acc = accuracy_score(y_test, y_pred)
    bacc = balanced_accuracy_score(y_test, y_pred)

    # Handle multiclass vs binary for f1
    is_binary = len(np.unique(y_test)) == 2
    f1 = f1_score(y_test, y_pred, average="weighted")

    roc_auc = None
    pr_auc = None

    if y_proba is not None and is_binary:
        try:
            # Need numeric labels for AUC; assume labels like 'high'/'low'.
            y_test_num = (y_test == model.classes_[1]).astype(int)
            roc_auc = roc_auc_score(y_test_num, y_proba)
            pr_auc = average_precision_score(y_test_num, y_proba)
        except Exception:
            pass

    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)

    return EvalResult(
        accuracy=acc,
        balanced_accuracy=bacc,
        f1=f1,
        roc_auc=roc_auc,
        pr_auc=pr_auc,
        confusion_matrix=cm,
        classification_report=cr,
    )


def format_metrics_table(
    metrics: dict[str, float], title: str = "Model Metrics"
) -> Table:
    """
    Create a rich-formatted table for metrics.

    Parameters
    ----------
    metrics : dict
        Dictionary of metric names to float values.
    title : str
        Table title.

    Returns
    -------
    rich.table.Table
        Formatted table ready for console printing.
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Score", justify="right", style="green")

    for name, value in metrics.items():
        if value is not None:
            # Format nicely
            pretty_name = name.replace("_", " ").title()
            table.add_row(pretty_name, f"{value:.4f}")

    return table


def compare_models(results: dict[str, EvalResult]) -> pd.DataFrame:
    """
    Create a comparison DataFrame of multiple models.

    Parameters
    ----------
    results : dict
        Mapping of model names to EvalResult objects.

    Returns
    -------
    pd.DataFrame
        DataFrame with models as rows and metrics as columns.
    """
    records = []
    for name, result in results.items():
        d = result.to_dict()
        d["model"] = name
        records.append(d)

    df = pd.DataFrame(records).set_index("model")
    return df
