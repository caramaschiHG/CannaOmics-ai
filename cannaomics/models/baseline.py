"""Baseline ML models for chemotype prediction."""

from collections.abc import Callable
from typing import Any

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier

try:
    from xgboost import XGBClassifier

    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False


def get_dummy_model(params: dict[str, Any] = None) -> DummyClassifier:
    """Get a stratified dummy classifier as an absolute baseline."""
    default_params = {"strategy": "stratified", "random_state": 42}
    if params:
        default_params.update(params)
    return DummyClassifier(**default_params)


def get_logistic_regression(params: dict[str, Any] = None) -> LogisticRegression:
    """Get a configured Logistic Regression model."""
    default_params = {"max_iter": 1000, "class_weight": "balanced", "random_state": 42}
    if params:
        default_params.update(params)
    return LogisticRegression(**default_params)


def get_random_forest(params: dict[str, Any] = None) -> RandomForestClassifier:
    """Get a configured Random Forest model."""
    default_params = {
        "n_estimators": 500,
        "max_depth": 6,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1,
    }
    if params:
        default_params.update(params)
    return RandomForestClassifier(**default_params)


def get_elastic_net(params: dict[str, Any] = None) -> SGDClassifier:
    """Get an Elastic Net model (via SGDClassifier)."""
    default_params = {
        "loss": "log_loss",  # Logistic regression
        "penalty": "elasticnet",
        "class_weight": "balanced",
        "random_state": 42,
        "max_iter": 1000,
    }
    if params:
        default_params.update(params)
    return SGDClassifier(**default_params)


def get_xgboost(params: dict[str, Any] = None):
    """Get an XGBoost classifier if available."""
    if not XGB_AVAILABLE:
        raise ImportError(
            "xgboost is not installed. Please install it with pip install xgboost"
        )

    default_params = {
        "n_estimators": 200,
        "max_depth": 4,
        "learning_rate": 0.05,
        "random_state": 42,
        "n_jobs": -1,
    }
    if params:
        default_params.update(params)
    return XGBClassifier(**default_params)


# Registry of available baseline models
MODEL_REGISTRY: dict[str, Callable] = {
    "dummy": get_dummy_model,
    "logistic_regression": get_logistic_regression,
    "random_forest": get_random_forest,
    "elastic_net": get_elastic_net,
    "xgboost": get_xgboost,
}


def get_model(name: str, params: dict[str, Any] = None):
    """
    Factory function to get a model by name.

    Parameters
    ----------
    name : str
        Name of the model ('random_forest', 'logistic_regression', etc.)
    params : dict, optional
        Hyperparameters to override defaults.

    Returns
    -------
    sklearn.base.BaseEstimator
        Configured scikit-learn compatible estimator.
    """
    name = name.lower()
    if name not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model '{name}'. Available: {list(MODEL_REGISTRY.keys())}"
        )

    return MODEL_REGISTRY[name](params)
