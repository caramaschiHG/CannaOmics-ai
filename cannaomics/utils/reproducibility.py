"""Reproducibility tracking and manifest generation."""

from __future__ import annotations

import json
import platform
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class ReproducibilityManifest:
    """Complete record of an analysis run for reproducibility."""

    run_id: str
    timestamp: str
    python_version: str
    package_versions: dict[str, str]
    dataset_ids: list[str]
    dataset_checksums: dict[str, str]
    random_seed: int
    model_params: dict[str, Any]
    metrics: dict[str, float]
    output_paths: list[str]
    git_commit: str | None = None
    config_file: str | None = None
    config_hash: str | None = None


def get_git_commit() -> str | None:
    """Retrieve the current git commit hash if available."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_package_versions() -> dict[str, str]:
    """Retrieve versions of key scientific packages."""
    versions: dict[str, str] = {}
    packages = ["pandas", "numpy", "scikit-learn", "xgboost", "shap", "biopython"]

    for pkg in packages:
        try:
            if pkg == "scikit-learn":
                import sklearn

                versions[pkg] = sklearn.__version__
            else:
                module = __import__(pkg)
                versions[pkg] = getattr(module, "__version__", "unknown")
        except ImportError:
            versions[pkg] = "not installed"

    return versions


def generate_manifest(
    run_id: str,
    dataset_ids: list[str],
    dataset_checksums: dict[str, str],
    random_seed: int,
    model_params: dict[str, Any],
    metrics: dict[str, float],
    output_paths: list[str],
    config_file: str | None = None,
    config_hash: str | None = None,
) -> ReproducibilityManifest:
    """Generate a full reproducibility manifest for a run."""
    return ReproducibilityManifest(
        run_id=run_id,
        timestamp=datetime.now(UTC).isoformat(timespec="seconds"),
        python_version=platform.python_version(),
        package_versions=get_package_versions(),
        dataset_ids=dataset_ids,
        dataset_checksums=dataset_checksums,
        random_seed=random_seed,
        model_params=model_params,
        metrics=metrics,
        output_paths=output_paths,
        git_commit=get_git_commit(),
        config_file=config_file,
        config_hash=config_hash,
    )


def save_manifest(manifest: ReproducibilityManifest, output_path: Path) -> None:
    """Save manifest to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(asdict(manifest), f, indent=2)


def load_manifest(path: Path) -> ReproducibilityManifest:
    """Load manifest from a JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return ReproducibilityManifest(**data)
