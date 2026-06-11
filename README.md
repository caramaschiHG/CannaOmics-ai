<div align="center">

# 🧬 CannaOmics AI

### From genome to chemotype, reproducibly.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-≥3.11-green.svg)](https://python.org)
[![Tests](https://github.com/caramaschiHG/CannaOmics-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/caramaschiHG/CannaOmics-ai/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Open-source bioinformatics and machine learning framework for integrating genomic, transcriptomic, and chemical data from *Cannabis sativa* — reproducing published findings and generating testable hypotheses about genes, variants, and patterns associated with terpene and cannabinoid production.**

[Scientific Background](#-scientific-scope) · [Quick Start](#-quick-start) · [Documentation](docs/) · [Roadmap](#-roadmap) · [Contributing](CONTRIBUTING.md)

</div>

---

## 🌿 Why This Exists

Cannabis chemotype research has exploded in the last decade. Dozens of studies have identified genetic loci, terpene synthase families, and regulatory regions that shape the chemical profile of different cultivars. But there's a problem:

> **The data is fragmented, the methods are not standardized, and there is no unified, open-source pipeline to reproduce these results — let alone build on them.**

Published papers report findings using different genomes, annotation versions, statistical thresholds, and feature engineering strategies. Replicating even a single paper's analysis often requires weeks of manual effort.

**CannaOmics AI changes that.** It is a reproducible research framework that ingests public data, normalizes it, and applies both classical bioinformatics and machine learning to systematically explore genotype–chemotype relationships.

---

## ⚡ What It Does

- 🧬 **Genomic variant analysis** — Ingests VCF/FASTA data, annotates variants in known terpene synthase and cannabinoid biosynthesis gene families
- 📊 **Transcriptome integration** — Normalizes RNA-seq expression data across studies and tissue types
- 🧪 **Chemical profile linking** — Maps chemotyping data (GC-MS, HPLC) to genomic features
- 🤖 **ML-powered hypothesis generation** — Trains interpretable models (Random Forest, XGBoost + SHAP) to rank candidate genes and variants
- 📋 **Automated reporting** — Generates publication-ready HTML reports with interactive visualizations
- 🔄 **Full reproducibility** — Every analysis step is logged, versioned, and re-runnable from a single manifest

---

## 🚫 What It Does NOT Do

> CannaOmics AI is a **research tool**, not a product or advisory service.

- 🚫 **No cultivation advice** — This is genomics software, not a grow guide
- 🚫 **No medical claims** — Outputs are statistical hypotheses, not clinical recommendations
- 🚫 **No proprietary data** — Uses only publicly available datasets and published research
- 🚫 **No strain optimization** — Does not design or recommend cultivar breeding strategies

---

## 🚀 Quick Start

```bash
# Install core framework
pip install cannaomics

# Install with all optional dependencies
pip install "cannaomics[all]"

# Run the demo pipeline
cannaomics demo --output results/demo/
```

For development:

```bash
# Clone the repository
git clone https://github.com/caramaschiHG/CannaOmics-ai.git
cd CannaOmics-ai

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode with all extras
pip install -e ".[all]"
pip install -r requirements-dev.txt  # or: pip install --dependency-groups dev,docs
```

---

## 🔬 Scientific Scope

CannaOmics AI focuses on reproducing and extending published findings for the following compound families.

### Target Terpenes

| Terpene | Class | Aroma Profile | Key Gene Families |
|:--|:--|:--|:--|
| **Myrcene** | Monoterpene | Earthy, musky | *TPS* (TPS-b) |
| **Limonene** | Monoterpene | Citrus | *TPS* (TPS-b) |
| **α-Pinene** | Monoterpene | Pine, sharp | *TPS* (TPS-b) |
| **β-Caryophyllene** | Sesquiterpene | Peppery, woody | *TPS* (TPS-a) |
| **Linalool** | Monoterpene | Floral, lavender | *TPS* (TPS-b, TPS-g) |
| **Humulene** | Sesquiterpene | Hoppy, earthy | *TPS* (TPS-a) |
| **Terpinolene** | Monoterpene | Herbal, fresh | *TPS* (TPS-b) |
| **Ocimene** | Monoterpene | Sweet, herbal | *TPS* (TPS-b, TPS-g) |

### Target Cannabinoids

| Cannabinoid | Precursor | Key Enzymes | Biosynthetic Pathway |
|:--|:--|:--|:--|
| **THCA** | CBGA | THCA synthase | MEP → GPP → CBGA → THCA |
| **CBDA** | CBGA | CBDA synthase | MEP → GPP → CBGA → CBDA |
| **CBGA** | OA + GPP | GOT (aromatic PT) | PKS → OA; MEP → GPP |
| **CBCA** | CBGA | CBCA synthase | MEP → GPP → CBGA → CBCA |
| **CBG** | CBGA | (decarboxylation) | Non-enzymatic from CBGA |

### Gene Families of Interest

- **TPS** — Terpene synthase superfamily (TPS-a, TPS-b, TPS-g subfamilies)
- **CYP450** — Cytochrome P450 oxidases involved in terpene modification
- **THCAS / CBDAS / CBCAS** — Cannabinoid oxidocyclases (FAD-dependent BBE-like)
- **OAC / OLS** — Olivetol/olivetolic acid cyclase and synthase (polyketide pathway)
- **GOT** — Geranylpyrophosphate:olivetolate geranyltransferase (aromatic prenyltransferase)
- **MEP pathway** — DXS, DXR, and downstream enzymes providing GPP precursor

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A["🌐 Public Data<br/>(NCBI, ENA, Zenodo)"] --> B["📥 Ingestion<br/>cannaomics.ingest"]
    B --> C["🔧 Normalization<br/>cannaomics.normalize"]
    C --> D["🏷️ Annotation<br/>cannaomics.annotate"]
    D --> E["📐 Feature Engineering<br/>cannaomics.features"]
    E --> F["🤖 ML Models<br/>cannaomics.ml"]
    F --> G["🔍 Interpretability<br/>SHAP · Feature Importance"]
    G --> H["📊 Candidate Ranking<br/>cannaomics.rank"]
    H --> I["📋 Report Generation<br/>HTML · PDF · CSV"]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#16213e,stroke:#0f3460,color:#fff
    style C fill:#16213e,stroke:#0f3460,color:#fff
    style D fill:#16213e,stroke:#0f3460,color:#fff
    style E fill:#16213e,stroke:#0f3460,color:#fff
    style F fill:#533483,stroke:#e94560,color:#fff
    style G fill:#533483,stroke:#e94560,color:#fff
    style H fill:#0f3460,stroke:#e94560,color:#fff
    style I fill:#1a1a2e,stroke:#53a653,color:#fff
```

---

## 📊 Example Output

After running the demo pipeline, the results directory will contain:

```
results/demo/
├── report.html               # Interactive HTML report
├── figures/
│   ├── feature_importance.png # Top-ranked features (SHAP)
│   ├── correlation_matrix.png # Gene expression × chemotype
│   └── variant_impact.png     # Variant effect sizes
├── tables/
│   ├── candidate_genes.csv    # Ranked gene list with scores
│   ├── variant_summary.csv    # Annotated variant table
│   └── model_metrics.csv      # Model performance summary
└── logs/
    └── pipeline.log           # Full execution log
```

---

## 🗺️ Roadmap

| Phase | Title | Duration | Status | Key Deliverables |
|:--:|:--|:--|:--:|:--|
| **0** | Repository Foundation | 1 week | ✅ | Project scaffold, CI/CD, dev toolchain |
| **1** | Data Ingestion & Schema | 2 weeks | 🔄 | NCBI/ENA downloaders, Pydantic schemas, manifest system |
| **2** | Genomics Module | 3 weeks | ⬜ | VCF parsing, variant annotation, gene family mapping |
| **3** | Transcriptomics Module | 2 weeks | ⬜ | RNA-seq normalization, differential expression, cross-study integration |
| **4** | Chemistry Module | 2 weeks | ⬜ | GC-MS/HPLC ingestion, compound mapping, chemotype classification |
| **5** | Feature Integration & ML | 3 weeks | ⬜ | Multi-omic feature matrix, RF/XGBoost models, SHAP explainability |
| **6** | Reporting & Visualization | 2 weeks | ⬜ | HTML report templates, interactive plots, publication figures |
| **7** | Validation & Release | 2 weeks | ⬜ | End-to-end tests, documentation site, PyPI release, paper draft |

> See [ROADMAP.md](ROADMAP.md) for detailed deliverables and milestones.

---

## 📖 Documentation

| Document | Description |
|:--|:--|
| [ROADMAP.md](ROADMAP.md) | Detailed phase-by-phase development plan |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute code, data, or annotations |
| [CHANGELOG.md](CHANGELOG.md) | Version history and release notes |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards and scientific integrity |
| [CITATION.cff](CITATION.cff) | How to cite this project |
| [docs/](docs/) | Full documentation (coming in Phase 7) |

---

## 🧪 Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=cannaomics --cov-report=html

# Lint and format
ruff check .
ruff format .

# Type checking
mypy cannaomics/
```

---

## 📄 Citation

If you use CannaOmics AI in your research, please cite:

```bibtex
@software{caramaschi2025cannaomics,
  author    = {Caramaschi, Sylvian},
  title     = {CannaOmics AI: Open-source framework for reproducible
               Cannabis sativa genotype-to-chemotype analysis},
  year      = {2025},
  url       = {https://github.com/caramaschiHG/CannaOmics-ai},
  license   = {Apache-2.0}
}
```

Or use the metadata in [`CITATION.cff`](CITATION.cff).

---

## 🤝 Credits

This project was born from a powerful scientific intuition:

> *If published research can identify genetic signals tied to chemical profiles, we can turn those methods into reproducible software and use AI to generate new, testable hypotheses.*

**Conceptual spark:** Leon  
**AI architecture, bioinformatics pipeline & open-source implementation:** Sylvian Caramaschi

---

## ⚖️ License

CannaOmics AI is released under the [Apache License 2.0](LICENSE).

You are free to use, modify, and distribute this software for any purpose — including commercial use — provided you include the original license and attribution.

---

<div align="center">

> *CannaOmics AI is not a black box. It is a reproducible research framework for generating testable hypotheses about Cannabis genotype-to-chemotype relationships.*

**Built with 🧬 for open science.**

</div>
