"""Model persistence and registry."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import joblib


@dataclass
class ModelMetadata:
    """Metadata for a saved model."""

    model_name: str
    model_type: str
    target_compound: str
    n_features: int
    n_samples: int
    metrics: dict
    training_date: str
    config_hash: str = ""


def save_model(model: Any, metadata: ModelMetadata, output_dir: Path) -> Path:
    """
    Save a model and its metadata to a directory.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        The trained model.
    metadata : ModelMetadata
        Metadata describing the model.
    output_dir : Path
        Directory to save to.

    Returns
    -------
    Path
        The directory where the model was saved.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save model binary
    model_path = output_dir / "model.joblib"
    joblib.dump(model, model_path)

    # Save metadata
    meta_path = output_dir / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(asdict(metadata), f, indent=2)

    return output_dir


def load_model(model_dir: Path) -> tuple[Any, ModelMetadata]:
    """
    Load a model and its metadata from a directory.

    Parameters
    ----------
    model_dir : Path
        Directory containing the saved model.

    Returns
    -------
    tuple
        (model, metadata)
    """
    model_path = model_dir / "model.joblib"
    meta_path = model_dir / "metadata.json"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    if not meta_path.exists():
        raise FileNotFoundError(f"Metadata file not found at {meta_path}")

    model = joblib.load(model_path)

    with open(meta_path) as f:
        meta_dict = json.load(f)
    metadata = ModelMetadata(**meta_dict)

    return model, metadata


def list_models(results_dir: Path) -> list[ModelMetadata]:
    """
    List all saved models in the results directory tree.

    Parameters
    ----------
    results_dir : Path
        Root directory to search for models.

    Returns
    -------
    list
        List of ModelMetadata objects found.
    """
    models = []
    for meta_path in results_dir.rglob("metadata.json"):
        # Check if there's a corresponding model.joblib
        if (meta_path.parent / "model.joblib").exists():
            try:
                with open(meta_path) as f:
                    meta_dict = json.load(f)
                models.append(ModelMetadata(**meta_dict))
            except Exception:
                pass  # Skip malformed metadata
    return models
