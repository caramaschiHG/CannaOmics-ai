"""Feature persistence for reproducible ML experiments.

This module provides save/load utilities for feature matrices, target
labels, and associated metadata.  Features are stored in Apache Parquet
format for efficient I/O, and metadata is persisted as JSON.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class FeatureMetadata:
    """Metadata describing a persisted feature set.

    Attributes
    ----------
    n_samples : int
        Number of samples in the feature matrix.
    n_features : int
        Number of features (columns) in the feature matrix.
    target_compound : str
        Name of the target chemical compound.
    target_method : str
        Method used to binarise the target (e.g., ``'median'``).
    feature_names : list[str]
        Ordered list of feature column names.
    creation_timestamp : str
        ISO-8601 timestamp of when the feature set was created.
    """

    n_samples: int
    n_features: int
    target_compound: str
    target_method: str
    feature_names: list[str]
    creation_timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        """Serialise metadata to a plain dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representation suitable for JSON serialisation.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FeatureMetadata:
        """Deserialise metadata from a dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            Dictionary produced by :meth:`to_dict`.

        Returns
        -------
        FeatureMetadata
            Reconstructed metadata instance.
        """
        return cls(**data)


def save_features(
    X: pd.DataFrame,
    y: pd.Series,
    metadata: FeatureMetadata,
    output_dir: str | Path,
) -> Path:
    """Persist a feature matrix, target labels, and metadata to disk.

    The following files are written to ``output_dir``:

    - ``features.parquet`` — feature matrix in Parquet format.
    - ``target.parquet`` — target series in Parquet format.
    - ``metadata.json`` — feature set metadata.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Target labels.
    metadata : FeatureMetadata
        Metadata describing the feature set.
    output_dir : str or Path
        Directory to write output files.  Created if it does not exist.

    Returns
    -------
    Path
        Path to the output directory.

    Raises
    ------
    IOError
        If files cannot be written to disk.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    features_path = output_dir / "features.parquet"
    target_path = output_dir / "target.parquet"
    metadata_path = output_dir / "metadata.json"

    logger.info("Saving feature set to %s", output_dir)

    X.to_parquet(features_path, index=True)
    logger.debug("Wrote features: %s (%d × %d)", features_path, *X.shape)

    y_df = y.to_frame(name=y.name or "target")
    y_df.to_parquet(target_path, index=True)
    logger.debug("Wrote target: %s (%d samples)", target_path, len(y))

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
    logger.debug("Wrote metadata: %s", metadata_path)

    logger.info(
        "Feature set saved: %d samples, %d features, compound='%s'",
        metadata.n_samples,
        metadata.n_features,
        metadata.target_compound,
    )

    return output_dir


def load_features(
    input_dir: str | Path,
) -> tuple[pd.DataFrame, pd.Series, dict[str, Any]]:
    """Load a persisted feature set from disk.

    Parameters
    ----------
    input_dir : str or Path
        Directory containing ``features.parquet``, ``target.parquet``,
        and ``metadata.json``.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series, dict[str, Any]]
        ``(X, y, metadata_dict)`` where *X* is the feature matrix, *y*
        is the target series, and *metadata_dict* is the raw metadata.

    Raises
    ------
    FileNotFoundError
        If any of the required files are missing.
    """
    input_dir = Path(input_dir)

    features_path = input_dir / "features.parquet"
    target_path = input_dir / "target.parquet"
    metadata_path = input_dir / "metadata.json"

    for path in (features_path, target_path, metadata_path):
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found: {path}. "
                f"Ensure the feature set was saved correctly in '{input_dir}'."
            )

    logger.info("Loading feature set from %s", input_dir)

    X = pd.read_parquet(features_path)
    logger.debug("Loaded features: %d × %d", *X.shape)

    y_df = pd.read_parquet(target_path)
    y = y_df.iloc[:, 0]
    y.name = y_df.columns[0]
    logger.debug("Loaded target: %d samples", len(y))

    with open(metadata_path, encoding="utf-8") as f:
        metadata_dict = json.load(f)
    logger.debug(
        "Loaded metadata for compound='%s'", metadata_dict.get("target_compound")
    )

    logger.info(
        "Feature set loaded: %d samples, %d features",
        X.shape[0],
        X.shape[1],
    )

    return X, y, metadata_dict
