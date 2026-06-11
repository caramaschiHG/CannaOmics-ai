"""Pydantic v2 configuration schema for CannaOmics pipelines.

Defines strongly-typed models for every section of the YAML configuration
file and provides a ``load_config`` helper that validates raw YAML against
the schema at import time.

Examples
--------
>>> from cannaomics.config.schema import load_config
>>> cfg = load_config(Path("pipeline.yaml"))
>>> cfg.project.name
'Cannabis Chemotype Predictor'
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Section models
# ---------------------------------------------------------------------------


class ProjectConfig(BaseModel):
    """Top-level project metadata.

    Attributes
    ----------
    name : str
        Human-readable project title.
    description : str
        One-line description of this analysis run.
    """

    name: str = "CannaOmics Analysis"
    description: str = ""


class DataConfig(BaseModel):
    """Paths and identifiers for input datasets.

    Attributes
    ----------
    dataset_id : str
        Unique identifier for the dataset (e.g. accession).
    chemical_profile_path : Path
        Path to the chemical-profile CSV / Parquet file.
    variant_matrix_path : Path
        Path to the variant-call matrix.
    sample_metadata_path : Path
        Path to the sample-level metadata table.
    """

    dataset_id: str = ""
    chemical_profile_path: Path = Path("data/chemical_profiles.csv")
    variant_matrix_path: Path = Path("data/variant_matrix.csv")
    sample_metadata_path: Path = Path("data/sample_metadata.csv")


class ThresholdConfig(BaseModel):
    """Configuration for binary classification thresholds.

    Attributes
    ----------
    method : {'median', 'quantile', 'absolute'}
        Strategy used to split continuous values into high / low.
    value : float, optional
        Explicit cut-off when *method* is ``'absolute'`` or the quantile
        fraction when *method* is ``'quantile'``.
    label_high : str
        Label assigned to values above the threshold.
    label_low : str
        Label assigned to values at or below the threshold.
    """

    method: Literal["median", "quantile", "absolute"] = "median"
    value: float | None = None
    label_high: str = "high"
    label_low: str = "low"


class TargetConfig(BaseModel):
    """Prediction-target specification.

    Attributes
    ----------
    compound : str
        Canonical compound name to predict (e.g. ``'beta_myrcene'``).
    task : {'classification', 'regression'}
        Machine-learning task type.
    threshold : ThresholdConfig
        Threshold settings for classification tasks.
    """

    compound: str = "beta_myrcene"
    task: Literal["classification", "regression"] = "classification"
    threshold: ThresholdConfig = Field(default_factory=ThresholdConfig)


class FeatureConfig(BaseModel):
    """Feature-engineering settings.

    Attributes
    ----------
    include : list[str]
        Glob patterns or explicit feature names to include.
    gene_families : list[str]
        Gene families to restrict features to.
    window_bp : int
        Window size (base-pairs) for gene-proximity annotation.
    missing_strategy : {'median', 'mean', 'zero', 'drop'}
        How to handle missing values in the feature matrix.
    """

    include: list[str] = Field(default_factory=lambda: ["*"])
    gene_families: list[str] = Field(
        default_factory=lambda: ["TPS", "cannabinoid_synthase", "MEP_pathway"]
    )
    window_bp: int = 50_000
    missing_strategy: Literal["median", "mean", "zero", "drop"] = "median"


class ModelConfig(BaseModel):
    """Machine-learning model configuration.

    Attributes
    ----------
    type : str
        Algorithm identifier.
    params : dict[str, Any]
        Keyword arguments forwarded to the model constructor.
    """

    type: Literal[
        "logistic_regression",
        "random_forest",
        "xgboost",
        "elastic_net",
        "dummy",
    ] = "random_forest"
    params: dict[str, Any] = Field(
        default_factory=lambda: {
            "n_estimators": 500,
            "max_depth": 8,
            "random_state": 42,
        }
    )


class ValidationConfig(BaseModel):
    """Cross-validation and evaluation settings.

    Attributes
    ----------
    split : {'stratified_kfold', 'train_test'}
        Splitting strategy.
    n_splits : int
        Number of folds (ignored for ``'train_test'``).
    test_size : float
        Fraction held out for testing (ignored for ``'stratified_kfold'``).
    metrics : list[str]
        Scoring metrics to compute.
    """

    split: Literal["stratified_kfold", "train_test"] = "stratified_kfold"
    n_splits: int = 5
    test_size: float = 0.2
    metrics: list[str] = Field(
        default_factory=lambda: [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "balanced_accuracy",
        ]
    )


class InterpretabilityConfig(BaseModel):
    """Interpretability / explainability settings.

    Attributes
    ----------
    methods : list[str]
        Explainability methods to apply (e.g. ``'feature_importance'``).
    top_n_candidates : int
        Number of top features to report.
    """

    methods: list[str] = Field(
        default_factory=lambda: [
            "feature_importance",
            "permutation_importance",
            "shap",
        ]
    )
    top_n_candidates: int = 25


class ReportConfig(BaseModel):
    """Output report settings.

    Attributes
    ----------
    output_dir : Path
        Directory for generated reports.
    formats : list[str]
        Output formats to produce.
    """

    output_dir: Path = Path("results/reports")
    formats: list[Literal["markdown", "html"]] = Field(
        default_factory=lambda: ["markdown", "html"]
    )


# ---------------------------------------------------------------------------
# Root model
# ---------------------------------------------------------------------------


class PipelineConfig(BaseModel):
    """Root configuration model for a CannaOmics pipeline run.

    Combines every section into a single validated object that can be
    serialised to / deserialised from YAML.

    Attributes
    ----------
    project : ProjectConfig
        Project metadata.
    data : DataConfig
        Input dataset paths.
    target : TargetConfig
        Prediction target specification.
    features : FeatureConfig
        Feature-engineering parameters.
    model : ModelConfig
        Model algorithm and hyper-parameters.
    validation : ValidationConfig
        Cross-validation strategy and metrics.
    interpretability : InterpretabilityConfig
        Explainability configuration.
    report : ReportConfig
        Report output settings.
    """

    project: ProjectConfig = Field(default_factory=ProjectConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    target: TargetConfig = Field(default_factory=TargetConfig)
    features: FeatureConfig = Field(default_factory=FeatureConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    interpretability: InterpretabilityConfig = Field(
        default_factory=InterpretabilityConfig
    )
    report: ReportConfig = Field(default_factory=ReportConfig)


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------


def load_config(path: Path) -> PipelineConfig:
    """Load and validate a YAML configuration file.

    Parameters
    ----------
    path : Path
        Filesystem path to the YAML file.

    Returns
    -------
    PipelineConfig
        Fully validated pipeline configuration.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    yaml.YAMLError
        If the file contains invalid YAML.
    pydantic.ValidationError
        If the YAML contents do not match the schema.

    Examples
    --------
    >>> cfg = load_config(Path("configs/defaults.yaml"))
    >>> cfg.model.type
    'random_forest'
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.safe_load(fh) or {}

    return PipelineConfig.model_validate(raw)
