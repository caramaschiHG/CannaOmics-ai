"""Path resolution and directory management."""

import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the absolute path to the project root directory."""
    # Assuming this file is at cannaomics/utils/paths.py
    return Path(__file__).parent.parent.parent.absolute()


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Parameters
    ----------
    path : Path
        Directory path to ensure.

    Returns
    -------
    Path
        The guaranteed-to-exist directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_data_dir() -> Path:
    """Get the primary data directory."""
    env_dir = os.environ.get("CANNAOMICS_DATA_DIR")
    if env_dir:
        return ensure_dir(Path(env_dir))
    return ensure_dir(get_project_root() / "data")


def get_results_dir() -> Path:
    """Get the primary results directory."""
    env_dir = os.environ.get("CANNAOMICS_RESULTS_DIR")
    if env_dir:
        return ensure_dir(Path(env_dir))
    return ensure_dir(get_project_root() / "results")


def get_configs_dir() -> Path:
    """Get the configuration templates directory."""
    return ensure_dir(get_project_root() / "configs")


def get_examples_dir() -> Path:
    """Get the examples directory."""
    return ensure_dir(get_project_root() / "examples")
