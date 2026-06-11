# Changelog

All notable changes to **CannaOmics AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Project scaffolding: `pyproject.toml`, CLI entry point, directory layout
- Comprehensive `README.md` with scientific scope, architecture diagram, and roadmap
- Apache 2.0 license, `CITATION.cff`, and `CODE_OF_CONDUCT.md`
- Contributing guide with scientific contribution guidelines
- `ROADMAP.md` covering Phase 0 → Phase 7
- Ruff linting configuration (numpy docstring convention, py311 target)
- Pytest + mypy configuration
- Data directory structure: `data/{raw,interim,processed,manifests}/`
- `.env.example` template for local configuration
- `.gitignore` tailored for Python, data science, and bioinformatics workflows

### Changed

- _Nothing yet._

### Fixed

- _Nothing yet._

---

## [0.1.0] — Phase 0: Repository Foundation

> **Status:** ✅ Complete

Initial release establishing the project foundation and developer experience.

### Added

- Repository structure and packaging with `hatchling`
- Core dependency specification (typer, rich, pandas, numpy, biopython, etc.)
- Optional dependency groups: `[ml]`, `[plotting]`, `[bio]`, `[all]`
- Development dependency groups: `dev`, `docs`, `notebooks`
- CLI skeleton via `cannaomics.cli:app`
- Full ruff + pytest + mypy toolchain configuration

---

[Unreleased]: https://github.com/caramaschiHG/CannaOmics-ai/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/caramaschiHG/CannaOmics-ai/releases/tag/v0.1.0
