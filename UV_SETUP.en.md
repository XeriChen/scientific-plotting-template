# UV Package Manager Configuration Guide

## Overview

This project is configured to support the modern `uv` package manager. `uv` is a blazingly fast Python package installer and resolver written in Rust, 10-100x faster than pip.

## Install UV

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Using pip
```bash
pip install uv
```

## Project Configuration

### Core Dependencies (pyproject.toml)

This project's `pyproject.toml` is optimized for minimal core dependencies for resource-constrained environments:

```toml
dependencies = [
    # Data processing (core)
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    
    # Visualization (core)
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    
    # Statistical analysis (core)
    "scipy>=1.11.0",
    "statsmodels>=0.14.0",
    
    # Machine learning (core)
    "scikit-learn>=1.3.0",
    
    # Utilities
    "tqdm>=4.65.0",
    "rich>=13.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "click>=8.0.0",
]
```

### Optional Dependencies

Additional features (interactive analysis, geospatial, advanced visualization, etc.) are moved to optional dependencies:

```toml
[project.optional-dependencies]
viz = [
    "plotly>=5.15.0",
    "bokeh>=3.2.0",
]
ml = [
    "xgboost>=1.7.0",
    "lightgbm>=4.0.0",
]
geo = [
    "geopandas>=0.13.0",
    "folium>=0.14.0",
]
# ... more optional dependencies in pyproject.toml
```

## Usage

### Create Virtual Environment and Install Dependencies

```bash
# Install only core dependencies (recommended for resource-constrained environments)
uv sync

# Install all dependencies (including dev dependencies)
uv sync --all-extras --dev

# Install specific optional dependencies
uv sync --extra viz --extra ml
```

### Run Commands

```bash
# Run command in virtual environment
uv run python your_script.py

# Run CLI tool
uv run spt --help

# Run tests
uv run pytest
```

### Add New Dependencies

```bash
# Add core dependency
uv add package-name

# Add optional dependency to specific group
uv add --optional viz package-name

# Add dev dependency
uv add --dev package-name
```

### Lock Dependencies

```bash
# Update lock file
uv lock

# Re-resolve all dependencies
uv lock --upgrade
```

## Environment Requirements

- **Python**: >= 3.9
- **Disk Space**: 
  - Minimal installation (core dependencies): ~500MB
  - Full installation (all dependencies): ~2GB+
- **Memory**: 2GB+ recommended

## Troubleshooting

### Insufficient Disk Space

If you encounter "No space left on device" error:

1. Clean uv cache:
   ```bash
   uv cache clean
   ```

2. Use no-cache mode:
   ```bash
   uv sync --no-cache
   ```

3. Install only core dependencies:
   ```bash
   uv sync  # without --all-extras
   ```

### Specify Cache Directory

```bash
export UV_CACHE_DIR=/path/to/larger/disk
uv sync
```

## Comparison with Traditional pip

| Feature | uv | pip |
|---------|-----|-----|
| Installation Speed | 10-100x faster | Baseline |
| Dependency Resolution | Very fast (Rust) | Slower (Python) |
| Disk Space | Global cache shared | Per-environment independent |
| Lock File | Native support (uv.lock) | Requires pip-tools |
| Python Management | Built-in (uv python) | Requires pyenv/conda |

## Best Practices

1. **Always commit `uv.lock`**: Ensure dependency consistency across team and environments
2. **Use optional dependencies**: Install on-demand to reduce initial download and installation time
3. **Leverage global cache**: uv automatically shares package cache across different projects
4. **Update regularly**: `uv lock --upgrade` keeps dependencies up-to-date

## Migrating from pip

If you previously used pip/virtualenv:

```bash
# Old way
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# New way (uv)
uv sync --dev
```

The virtual environments created by both are compatible and can be used interchangeably.
