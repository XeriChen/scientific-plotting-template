# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A modern Python data analysis and visualization workspace template designed for scientific computing and data science workflows.

## Code Architecture

The project follows a modular package structure under `src/scientific_template/`:

- **`data/`** - Data processing and I/O utilities (pandas, polars, file formats)
- **`plotting/`** - Visualization tools (matplotlib, seaborn, plotly, bokeh)
- **`stats/`** - Statistical analysis functions (scipy, statsmodels, pingouin)
- **`ml/`** - Machine learning utilities (scikit-learn, xgboost, lightgbm)
- **`utils/`** - General utility functions and helpers

Each module contains an `__init__.py` for package initialization and exports.

## Common Development Commands

### Package Management
- `uv add <package>` - Add a new dependency
- `uv remove <package>` - Remove a dependency
- `uv sync` - Sync dependencies
- `uv lock` - Update lock file

### Code Quality
- `ruff check .` - Run linter
- `ruff format .` - Format code
- `black .` - Alternative code formatting
- `mypy src/` - Type checking
- `pyright` - Alternative type checking

### Testing
- `pytest` - Run all tests with coverage
- `pytest tests/test_module.py` - Run specific test file
- `pytest -k "test_function"` - Run specific test by name
- `pytest --cov-report=html` - Generate HTML coverage report

### Development Environment
- `uv run python -m scientific_template` - Run the package
- `uv run pytest` - Run tests with uv
- `uv run jupyter lab` - Start Jupyter Lab
- `uv run spt` - Run CLI tool

### Build & Distribution
- `uv build` - Build package
- `hatch build` - Alternative build command
- `hatch publish` - Publish to PyPI

## Project Structure

```
src/scientific_template/
├── __init__.py          # Package initialization
├── cli.py              # CLI entry point (referenced in pyproject.toml)
├── data/               # Data processing
├── plotting/           # Visualization
├── stats/              # Statistics
├── ml/                 # Machine learning
└── utils/              # Utilities

tests/                  # Test suite
docs/                   # Documentation
examples/               # Example scripts
notebooks/              # Jupyter notebooks
data/                   # Sample data
```

## Configuration

- **`pyproject.toml`** - Main configuration file (build, dependencies, tool settings)
- **Ruff** - Configured with extensive rule set, ignores common false positives
- **Pytest** - Configured with coverage, parallel execution support
- **Type checking** - Both mypy and pyright configured for strict mode

## Key Dependencies

### Data Processing
- pandas, polars, numpy for data manipulation
- pyarrow, fastparquet for efficient file I/O

### Visualization
- matplotlib, seaborn for static plots
- plotly, plotly-express for interactive visualizations
- bokeh for web-based dashboards

### Analysis
- scipy, statsmodels, pingouin for statistics
- scikit-learn, xgboost, lightgbm for ML

### Development
- ruff, black for code quality
- pytest, mypy for testing and type checking
- jupyter, notebook for interactive analysis

## Working with the Codebase

1. Use `uv` for all Python package management tasks
2. Run `ruff check` before committing to catch style issues
3. Write tests in the `tests/` directory following pytest conventions
4. Add new modules under the appropriate subpackage (data, plotting, etc.)
5. Use type hints throughout for better IDE support and error checking
6. For CLI additions, modify the `cli.py` entry point in the package root

## Testing Strategy

- Unit tests for individual functions in each module
- Integration tests for cross-module functionality
- Example notebooks in `notebooks/` demonstrate usage patterns
- `examples/` directory contains runnable demonstration scripts

## Development Workflow

1. Create feature branch: `git checkout -b feature-name`
2. Make changes with tests
3. Run linting: `ruff check . && ruff format --check .`
4. Run tests: `pytest`
5. Check types: `mypy src/`
6. Commit changes
7. Create pull request