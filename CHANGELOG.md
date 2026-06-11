# Changelog

All notable changes to **CannaOmics AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Windows console hardening: force UTF-8 stdout/stderr and disable Rich's
  legacy-windows renderer so non-BMP emoji (e.g. 🧬) no longer crash `cannaomics --help`
- Backward-compatible alias `cannaomics.utils.checksums.generate_manifest`
  while introducing the disambiguated `generate_file_manifest`

### Changed

- Demo report template now uses Jinja whitespace control so generated
  Markdown tables render without blank rows between data lines
- Demo metadata records real ISO-8601 training timestamp (was literal `"today"`)
- Greek-letter compound synonyms are now normalised on the fly via a
  translation table, eliminating duplicate dictionary keys and ambiguous-unicode lint warnings
- Reproducibility manifest uses timezone-aware UTC timestamps (replaces deprecated `datetime.utcnow()`)
- README roadmap table now mirrors `ROADMAP.md` (Phase 0–7) to remove
  inconsistent phase descriptions
- `pyproject.toml` ignores `B008` for `cannaomics/cli.py` (Typer
  `Option(...)` defaults are an idiomatic, not buggy, pattern)

### Fixed

- `cannaomics --help` and `cannaomics --version` crashing on Windows
  cp1252 consoles (`UnicodeEncodeError` on the 🧬 emoji)
- Broken Markdown tables in the demo report (blank rows between data lines)
- Implicit-`Optional` annotations across `baseline.py`, `demo.py`,
  `utils/logging.py`, `utils/checksums.py`
- Five `raise ... from err` propagation gaps in `cli.py` exception handlers
- Hard-coded `training_date="today"` and empty `config_hash=""` placeholders in the demo
- Typo "Raking de Candidatos" → "Ranking de Candidatos" in the README
- Wrong `CITATION.cff` release date (2025-06-11 → 2026-06-11)
- Removed `time.sleep()` "fake loading" calls from the demo pipeline
- Removed unused `plotly.graph_objects` import in `interpretability/plots.py`
- Replaced ambiguous unicode (`×`, `α`, `β`, `δ`) in log messages and code with ASCII equivalents

---

## [0.1.0] - Phase 0: Repository Foundation

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
