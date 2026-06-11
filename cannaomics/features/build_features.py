"""Feature matrix construction and data preparation for ML pipelines.

This module provides utilities for building feature matrices from variant
and chemical data, handling missing values, feature selection, and data
splitting strategies for cross-validation.
"""

from __future__ import annotations

import logging
from collections.abc import Generator

import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import StratifiedKFold, train_test_split

logger = logging.getLogger(__name__)


def build_feature_matrix(
    variant_df: pd.DataFrame,
    chemical_df: pd.DataFrame,
    target_compound: str,
    target_method: str = "median",
    label_high: str = "high",
    label_low: str = "low",
) -> tuple[pd.DataFrame, pd.Series]:
    """Build an aligned feature matrix and binary target from variant and chemical data.

    Aligns samples present in both ``variant_df`` and ``chemical_df``,
    then binarises the target compound concentration into *high* / *low*
    labels using the chosen aggregation method.

    Parameters
    ----------
    variant_df : pd.DataFrame
        Variant feature matrix with samples as rows (index) and variant
        features as columns.
    chemical_df : pd.DataFrame
        Chemical quantification table with samples as rows (index) and
        compound names as columns.
    target_compound : str
        Name of the chemical compound column to use as the prediction
        target.
    target_method : str, optional
        Thresholding method for binarisation. One of ``'median'``,
        ``'mean'``, or ``'quantile75'``.  Default is ``'median'``.
    label_high : str, optional
        Label assigned to samples above the threshold.  Default ``'high'``.
    label_low : str, optional
        Label assigned to samples at or below the threshold.  Default
        ``'low'``.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series]
        ``(X, y)`` where *X* is the aligned feature matrix and *y* is the
        binary target series.

    Raises
    ------
    ValueError
        If ``target_compound`` is not found in ``chemical_df``, or no
        overlapping samples exist, or ``target_method`` is invalid.
    """
    if target_compound not in chemical_df.columns:
        raise ValueError(
            f"Target compound '{target_compound}' not found in chemical_df. "
            f"Available compounds: {list(chemical_df.columns)}"
        )

    # Align samples present in both datasets
    common_samples = variant_df.index.intersection(chemical_df.index)
    if len(common_samples) == 0:
        raise ValueError(
            "No overlapping samples between variant_df and chemical_df. "
            "Ensure both DataFrames share a common sample index."
        )

    logger.info(
        "Aligning %d common samples (variant=%d, chemical=%d)",
        len(common_samples),
        len(variant_df),
        len(chemical_df),
    )

    X = variant_df.loc[common_samples].copy()
    compound_values = chemical_df.loc[common_samples, target_compound].astype(float)

    # Compute threshold
    valid_values = compound_values.dropna()
    if len(valid_values) == 0:
        raise ValueError(
            f"All values for '{target_compound}' are NaN in common samples."
        )

    if target_method == "median":
        threshold = valid_values.median()
    elif target_method == "mean":
        threshold = valid_values.mean()
    elif target_method == "quantile75":
        threshold = valid_values.quantile(0.75)
    else:
        raise ValueError(
            f"Unknown target_method '{target_method}'. "
            "Choose from 'median', 'mean', 'quantile75'."
        )

    logger.info(
        "Binarising '%s' with method='%s' (threshold=%.4f)",
        target_compound,
        target_method,
        threshold,
    )

    y = pd.Series(
        np.where(compound_values > threshold, label_high, label_low),
        index=common_samples,
        name=target_compound,
    )

    class_counts = y.value_counts()
    logger.info("Class distribution: %s", class_counts.to_dict())

    return X, y


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "median",
) -> pd.DataFrame:
    """Impute missing values in a numeric feature DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Feature matrix potentially containing NaN values.
    strategy : str, optional
        Imputation strategy.  One of ``'median'``, ``'mean'``, ``'zero'``,
        or ``'drop'``.  Default is ``'median'``.

    Returns
    -------
    pd.DataFrame
        DataFrame with missing values imputed (or rows/columns dropped).

    Raises
    ------
    ValueError
        If ``strategy`` is not recognised.
    """
    n_missing = df.isna().sum().sum()
    if n_missing == 0:
        logger.info("No missing values detected.")
        return df.copy()

    logger.info("Handling %d missing values with strategy='%s'", n_missing, strategy)

    result = df.copy()

    if strategy == "median":
        fill_values = result.median(numeric_only=True)
        result = result.fillna(fill_values)
    elif strategy == "mean":
        fill_values = result.mean(numeric_only=True)
        result = result.fillna(fill_values)
    elif strategy == "zero":
        result = result.fillna(0)
    elif strategy == "drop":
        before = len(result)
        result = result.dropna()
        logger.info("Dropped %d rows containing NaN values.", before - len(result))
    else:
        raise ValueError(
            f"Unknown imputation strategy '{strategy}'. "
            "Choose from 'median', 'mean', 'zero', 'drop'."
        )

    return result


def select_features(
    X: pd.DataFrame,
    y: pd.Series,
    method: str = "variance",
    n_features: int | None = None,
) -> pd.DataFrame:
    """Select informative features from the feature matrix.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix (samples × features).
    y : pd.Series
        Target labels (used for future supervised methods; currently
        unused for ``'variance'`` method).
    method : str, optional
        Feature selection method.  Currently supports ``'variance'``
        (removes zero-variance features).  Default is ``'variance'``.
    n_features : int or None, optional
        Maximum number of features to retain.  If ``None``, all
        non-zero-variance features are kept.  Default is ``None``.

    Returns
    -------
    pd.DataFrame
        Filtered feature matrix with selected columns only.

    Raises
    ------
    ValueError
        If ``method`` is not recognised.
    """
    original_n = X.shape[1]

    if method == "variance":
        selector = VarianceThreshold(threshold=0.0)
        selector.fit(X)
        mask = selector.get_support()
        selected_cols = X.columns[mask]
        result = X[selected_cols].copy()
    else:
        raise ValueError(
            f"Unknown feature selection method '{method}'. "
            "Currently supported: 'variance'."
        )

    if n_features is not None and len(result.columns) > n_features:
        # Keep top-n by variance
        variances = result.var()
        top_cols = variances.nlargest(n_features).index
        result = result[top_cols]

    logger.info(
        "Feature selection (%s): %d -> %d features",
        method,
        original_n,
        result.shape[1],
    )

    return result


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    method: str = "stratified_kfold",
    n_splits: int = 5,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Generator[tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series], None, None]:
    """Generate train/test splits using the specified strategy.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Target labels.
    method : str, optional
        Splitting strategy.  One of ``'stratified_kfold'`` or
        ``'holdout'``.  Default is ``'stratified_kfold'``.
    n_splits : int, optional
        Number of folds for k-fold methods.  Default is ``5``.
    test_size : float, optional
        Proportion of data for test set in holdout split.  Default ``0.2``.
    random_state : int, optional
        Random seed for reproducibility.  Default ``42``.

    Yields
    ------
    tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        ``(X_train, X_test, y_train, y_test)`` for each split.

    Raises
    ------
    ValueError
        If ``method`` is not recognised.
    """
    if method == "stratified_kfold":
        skf = StratifiedKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=random_state,
        )
        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y)):
            logger.debug(
                "Fold %d: train=%d, test=%d",
                fold_idx + 1,
                len(train_idx),
                len(test_idx),
            )
            X_train = X.iloc[train_idx]
            X_test = X.iloc[test_idx]
            y_train = y.iloc[train_idx]
            y_test = y.iloc[test_idx]
            yield X_train, X_test, y_train, y_test

    elif method == "holdout":
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            stratify=y,
            random_state=random_state,
        )
        yield X_train, X_test, y_train, y_test

    else:
        raise ValueError(
            f"Unknown split method '{method}'. "
            "Choose from 'stratified_kfold', 'holdout'."
        )
