# Contributing to CannaOmics AI

First off, thank you for considering contributing to CannaOmics AI! It's people like you that make open-source scientific tools possible.

## 🔬 Scientific Contributions

CannaOmics AI is a bioinformatics and machine learning framework. We welcome scientific contributions, including:
- Adding support for new public datasets.
- Curating gene lists (e.g., adding verified Terpene Synthase genes).
- Enhancing normalization dictionaries for chemical compounds.
- Adding statistical or biological interpretability methods.

### 🚫 Out-of-Scope Contributions
To maintain scientific and ethical integrity, we **will not accept** contributions related to:
- Cultivation advice, yield optimization, or growing protocols.
- Medical or therapeutic claims.
- Optimization of controlled substance production.
- Modifications that remove our limitations and disclaimers.

## 🚀 Development Setup

We use `hatchling` for building and `uv` or `pip` for dependency management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/caramaschiHG/CannaOmics-ai.git
   cd CannaOmics-ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install the package in editable mode with all dev dependencies:**
   ```bash
   pip install -e ".[all,dev]"
   ```

4. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## 💅 Code Style

We use `ruff` to format and lint our code. We follow the NumPy docstring convention.

- To check your code:
  ```bash
  ruff check .
  ```
- To format your code:
  ```bash
  ruff format .
  ```

## 🧪 Testing

We use `pytest` for running our test suite. All new features should include corresponding tests.

- To run the tests:
  ```bash
  pytest
  ```

## 🛠️ Pull Request Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code passes the `ruff` linter and formatter.
6. Issue that pull request!

## 📖 Building Documentation

We use `mkdocs-material` for documentation.

- To serve the docs locally:
  ```bash
  pip install -e ".[docs]"
  mkdocs serve
  ```
