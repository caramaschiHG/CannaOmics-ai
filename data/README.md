# Data Directory

This directory contains the datasets used by CannaOmics AI. Data is organized according to the cookiecutter data science standard.

## Structure

- `raw/`: Immutable, original raw datasets downloaded from external sources (e.g., Dryad). Never modified.
- `interim/`: Intermediate data that has been transformed but is not yet ready for modeling.
- `processed/`: Final, clean datasets used for modeling.
- `manifests/`: JSON manifests tracking the provenance, checksums, and versions of the downloaded datasets.

*Note: For the demo pipeline, synthetic data is located in the `examples/` directory.*
