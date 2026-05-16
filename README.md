# Scientific Plotting Template

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-red.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: mypy](https://img.shields.io/badge/type%20checked-mypy-orange.svg)](http://mypy-lang.org/)

**A modern Python data analysis and visualization workspace**

</div>

---

## 📖 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Modules Overview](#-modules-overview)
- [Examples](#-examples)
- [CLI Tool](#-cli-tool)
- [Configuration](#-configuration)
- [Development](#-development)
- [License](#-license)

---

## 🎯 Introduction

**Scientific Plotting Template** is a feature-complete Python data analysis and visualization workspace template designed specifically for scientific computing and data science workflows. It integrates a complete solution for data processing, statistical analysis, machine learning, and visualization.

### Core Value

- 🔧 **Out-of-the-box** - Pre-configured best practices and toolchain
- 📊 **Full-featured** - Complete workflow from data loading to model deployment
- 🚀 **High-performance** - Supports both pandas and polars backends
- 📦 **Modular design** - Clear layered architecture, easy to extend
- 🎨 **Publication-quality** - Multiple plotting libraries and styles supported

---

## ✨ Features

### Data Processing
- ✅ Multi-format data loading (CSV, Excel, JSON, Parquet, Feather)
- ✅ Data cleaning and validation (missing values, outliers, data types)
- ✅ Data transformation and reshaping (normalization, encoding, binning)
- ✅ Supports pandas and polars dual-engine

### Statistical Analysis
- ✅ Descriptive statistics
- ✅ Hypothesis testing (t-test, ANOVA, chi-square test)
- ✅ Correlation analysis (Pearson, Spearman)
- ✅ Normality testing
- ✅ Confidence interval calculation

### Machine Learning
- ✅ Model training pipeline
- ✅ Cross-validation
- ✅ Grid search hyperparameter tuning
- ✅ Classification and regression metrics evaluation
- ✅ Supports scikit-learn, XGBoost, LightGBM

### Visualization
- ✅ 7+ chart types (line, scatter, bar, histogram, boxplot, heatmap, etc.)
- ✅ Supports matplotlib, seaborn, plotly, bokeh
- ✅ Publication-quality image output (300 DPI)
- ✅ Customizable styles and themes

### Utilities
- ✅ Logging configuration
- ✅ YAML/JSON configuration management
- ✅ Performance timer
- ✅ Command-line interface (CLI)

---

## 📥 Installation

### Basic Installation

```bash
# Clone repository
git clone https://github.com/yourusername/scientific-plotting-template.git
cd scientific-plotting-template

# Install with pip
pip install -e .

# Or use uv (recommended)
uv pip install -e .
```

### Full Installation (including all dependencies)

```bash
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

```python
from scientific_template import (
    DataLoader, DataProcessor, Plotter, 
    StatisticalAnalyzer, ModelPipeline,
    setup_logging, load_config
)

# Setup
logger = setup_logging(level="INFO")
config = load_config("config.yaml")

# Load and process data
loader = DataLoader(engine="pandas")
df = loader.load_csv("data/input/sales_data.csv")

processor = DataProcessor()
df_clean = processor.handle_missing(df, strategy="fill_mean")

# Analyze and visualize
analyzer = StatisticalAnalyzer()
print(analyzer.descriptive_stats(df_clean))

plotter = Plotter(style="seaborn-v0_8")
fig = plotter.create_histogram(df_clean, column="sales")
plotter.save_figure(fig, "output/figures/sales.png")
```

---

## 📁 Project Structure

```
scientific-plotting-template/
├── src/scientific_template/    # Main package
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # Command-line interface
│   ├── data/                   # Data processing
│   ├── plotting/               # Visualization
│   ├── stats/                  # Statistics
│   ├── ml/                     # Machine learning
│   └── utils/                  # Utilities
├── data/                       # Sample data
├── output/                     # Analysis output
├── examples/                   # Example scripts
├── notebooks/                  # Jupyter notebooks
├── tests/                      # Test suite
├── logs/                       # Log files
├── config.yaml                 # Configuration
└── pyproject.toml              # Project config
```

---

## 📦 Modules Overview

### Data Module
| Class | Function |
|-------|----------|
| `DataLoader` | Multi-format data loading |
| `DataProcessor` | Data processing operations |
| `DataCleaner` | Data cleaning and validation |
| `DataTransformer` | Data transformation |

### Plotting Module
| Class | Function |
|-------|----------|
| `Plotter` | Main plotting class |

### Statistics Module
| Class | Function |
|-------|----------|
| `StatisticalAnalyzer` | Statistical analysis |

### ML Module
| Class | Function |
|-------|----------|
| `ModelPipeline` | ML training pipeline |
| `CrossValidator` | Cross-validation |

---

## 📝 Examples

Explore the `examples/` directory for usage examples:
- `01_full_analysis.py` - Complete data analysis workflow
- `02_benchmark_analysis.py` - Performance benchmark analysis

---

## 🛠️ CLI Tool

```bash
spt --help
spt init
spt info --input data/file.csv
spt config-style --style seaborn-v0_8
```

---

## 👨‍💻 Development

```bash
# Install dev dependencies
pip install -e ".[dev,test]"

# Run tests
pytest --cov=scientific_template

# Lint and format
ruff check .
ruff format .
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ❤️ for the scientific Python community**

</div>
