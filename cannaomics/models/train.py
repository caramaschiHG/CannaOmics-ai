"""Model training and cross-validation orchestration."""

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    make_scorer,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

from .baseline import get_model


@dataclass
class TrainResult:
    """Results from a model training run."""

    model: Any
    cv_scores: dict[str, list[float]]
    mean_scores: dict[str, float]
    feature_names: list[str]
    training_time: float
    n_samples: int
    n_features: int


def cross_validate_model(
    model: Any, X: pd.DataFrame, y: pd.Series, n_splits: int = 5, random_state: int = 42
) -> dict[str, list[float]]:
    """
    Perform stratified k-fold cross-validation.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        The model to evaluate.
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Target vector.
    n_splits : int, optional
        Number of CV folds, default 5.
    random_state : int, optional
        Random seed for fold generation.

    Returns
    -------
    dict
        Dictionary of metric arrays across folds.
    """
    # Define scorers
    scoring = {
        "accuracy": make_scorer(accuracy_score),
        "balanced_accuracy": make_scorer(balanced_accuracy_score),
        "f1": make_scorer(f1_score, average="weighted"),
    }

    # Try to add ROC AUC if probabilities are supported
    if hasattr(model, "predict_proba"):
        try:
            # Basic try-catch in case of binary vs multiclass issues
            scoring["roc_auc"] = make_scorer(
                roc_auc_score, response_method="predict_proba", multi_class="ovr"
            )
        except Exception:
            pass

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    # Run CV
    cv_results = cross_validate(
        model, X, y, cv=cv, scoring=scoring, return_train_score=False, n_jobs=-1
    )

    # Clean up results dictionary (remove 'test_' prefix)
    clean_results = {
        k.replace("test_", ""): list(v)
        for k, v in cv_results.items()
        if k.startswith("test_")
    }
    return clean_results


def train_final_model(model: Any, X: pd.DataFrame, y: pd.Series) -> Any:
    """Train model on the full dataset."""
    model.fit(X, y)
    return model


def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    model_name: str,
    model_params: dict[str, Any] | None = None,
    n_splits: int = 5,
    random_state: int = 42,
) -> TrainResult:
    """
    Orchestrate full training and evaluation of a model.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Target vector.
    model_name : str
        Name of model from registry.
    model_params : dict, optional
        Hyperparameters.
    n_splits : int, optional
        Number of cross-validation folds.

    Returns
    -------
    TrainResult
        Comprehensive training result object.
    """
    start_time = time.time()

    # 1. Get model
    model = get_model(model_name, model_params)

    # 2. Cross-validate
    cv_scores = cross_validate_model(
        model, X, y, n_splits=n_splits, random_state=random_state
    )

    # Calculate means
    mean_scores = {k: float(np.mean(v)) for k, v in cv_scores.items()}

    # 3. Train final model on all data
    final_model = train_final_model(model, X, y)

    training_time = time.time() - start_time

    return TrainResult(
        model=final_model,
        cv_scores=cv_scores,
        mean_scores=mean_scores,
        feature_names=list(X.columns),
        training_time=training_time,
        n_samples=len(X),
        n_features=X.shape[1],
    )
