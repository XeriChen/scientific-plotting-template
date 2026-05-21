# Scientific Template Usage Documentation

## 📖 Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Module Details](#module-details)
  - [Data Module](#data-module)
  - [Plotting Module](#plotting-module)
  - [Statistics Module](#statistics-module)
  - [Machine Learning Module](#machine-learning-module)
  - [Utilities Module](#utilities-module)
- [CLI Tool](#cli-tool)
- [Configuration Management](#configuration-management)
- [Best Practices](#best-practices)
- [Example Code](#example-code)

---

## Introduction

**Scientific Template** is a modern Python data analysis and visualization workspace that provides a complete toolkit for:

- 📊 **Data Processing**: Multi-format loading, cleaning, and transformation
- 📈 **Visualization**: Publication-quality scientific charts
- 📉 **Statistical Analysis**: Common statistical tests and analysis
- 🤖 **Machine Learning**: Streamlined model training and evaluation
- 🛠️ **Utilities**: Logging, configuration, timers, and more

### Core Features

- **Dual Backend Support**: Compatible with both pandas and polars
- **Modular Design**: Clear module separation for easy extension
- **Type Safe**: Complete type annotations with static type checking support
- **CLI Tools**: Convenient command-line interface
- **Best Practices**: Follows standards for scientific computing and reproducible research

---

## Installation

### Basic Installation

```bash
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

### Optional Dependencies

```bash
# Install only test dependencies
pip install -e ".[test]"

# Install only documentation dependencies
pip install -e ".[docs]"
```

### Requirements

- Python >= 3.9
- Main dependencies: pandas, numpy, matplotlib, seaborn, scipy, scikit-learn

---

## Quick Start

```python
from scientific_template import (
    DataLoader, DataProcessor, Plotter, 
    StatisticalAnalyzer, ModelPipeline,
    setup_logging, load_config
)

# 1. Setup logging
logger = setup_logging(level="INFO")

# 2. Load data
loader = DataLoader(engine="pandas")
df = loader.load_csv("data/my_data.csv")

# 3. Data processing
processor = DataProcessor()
df_clean = processor.remove_duplicates(df)
df_clean = processor.handle_missing(df_clean, strategy="fill_mean")

# 4. Descriptive statistics
analyzer = StatisticalAnalyzer()
stats = analyzer.descriptive_stats(df_clean)
print(stats)

# 5. Visualization
plotter = Plotter(style="seaborn-v0_8")
fig = plotter.create_line_plot(
    data=df_clean,
    x="time",
    y="value",
    title="Time Series Analysis"
)

# 6. Save figure
plotter.save_figure(fig, "output/analysis.png")
```

---

## Module Details

### Data Module

The data module provides a complete data processing pipeline including loading, cleaning, processing, and transformation.

#### DataLoader - Data Loader

Supports automatic detection and loading of multiple file formats.

```python
from scientific_template.data import DataLoader

# Initialize (supports pandas or polars backend)
loader = DataLoader(engine="pandas")  # or engine="polars"

# Auto-detect format loading
df = loader.load("data/file.csv")
df = loader.load("data/file.xlsx")
df = loader.load("data/file.json")
df = loader.load("data/file.parquet")

# Load with specified format
df = loader.load_csv("data/file.csv", sep=",")
df = loader.load_excel("data/file.xlsx", sheet_name="Sheet1")
df = loader.load_json("data/file.json")
df = loader.load_parquet("data/file.parquet")
```

**Supported Formats**:
- CSV / TSV
- Excel (.xlsx, .xls)
- JSON
- Parquet
- Feather

#### DataProcessor - Data Processor

Provides common data processing operations.

```python
from scientific_template.data import DataProcessor

processor = DataProcessor(engine="pandas")

# Remove duplicates
df = processor.remove_duplicates(df, subset=["col1", "col2"], keep="first")

# Handle missing values
df = processor.handle_missing(df, strategy="drop")
df = processor.handle_missing(df, strategy="fill_mean")
df = processor.handle_missing(df, strategy="fill_median")
df = processor.handle_missing(df, strategy="fill_mode")
df = processor.handle_missing(df, strategy="fill_value", fill_value=0)

# Rename columns
df = processor.rename_columns(df, {"old_name": "new_name"})

# Select columns
df = processor.select_columns(df, ["col1", "col2"])

# Filter rows
df = processor.filter_rows(df, lambda x: x["value"] > 100)

# Sort
df = processor.sort_values(df, by="value", ascending=False)

# Add new column
df = processor.add_column(df, "new_col", values=0)
df = processor.add_column(df, "computed", lambda row: row["a"] + row["b"])

# Get data info
info = processor.get_info(df)
print(info)
```

#### DataCleaner - Data Cleaner

Handles data quality issues and standardization.

```python
from scientific_template.data import DataCleaner

cleaner = DataCleaner(engine="pandas")

# Standardize column names
df = cleaner.standardize_column_names(df, case="snake")

# Remove whitespace
df = cleaner.remove_whitespace(df, columns=["name", "address"])

# Fix data types
df = cleaner.fix_data_types(df, column_types={"age": "int", "price": "float"})

# Remove special characters
df = cleaner.remove_special_characters(df, columns=["text"], pattern=r'[^a-zA-Z0-9\s]')

# Validate emails
df = cleaner.validate_email(df, column="email", remove_invalid=True)

# Detect outliers (IQR method)
outliers = cleaner.detect_outliers_iqr(df, columns=["value"], multiplier=1.5)

# Clean currency columns
df = cleaner.clean_currency(df, columns=["price"])  # "$1,234.56" -> 1234.56
```

#### DataTransformer - Data Transformer

Data transformation and reshaping operations.

```python
from scientific_template.data import DataTransformer

transformer = DataTransformer(engine="pandas")

# Normalization
df = transformer.normalize(df, method="minmax")
df = transformer.normalize(df, method="zscore")
df = transformer.normalize(df, method="robust")

# Encode categorical variables
df = transformer.encode_categorical(df, columns=["category"], method="onehot")
df = transformer.encode_categorical(df, method="label")
df = transformer.encode_categorical(df, method="frequency")

# Pivot table
pivot_df = transformer.pivot(df, index="date", columns="category", values="value", aggfunc="mean")

# Melt (wide to long format)
long_df = transformer.melt(df, id_vars=["id"], value_vars=["col1", "col2"])

# Binning
df = transformer.binning(df, column="age", bins=5, labels=["young", "mid", "old"])

# Log transformation
df = transformer.log_transform(df, columns=["income"], base=np.e)

# Rolling window
rolling_mean = transformer.rolling_window(df, column="value", window=7, operation="mean")
```

---

### Plotting Module

Tools for creating publication-quality visualizations.

#### Plotter - Plotting Class

```python
from scientific_template.plotting import Plotter

# Initialize
plotter = Plotter(style="seaborn-v0_8", context="notebook")

# Line plot
fig = plotter.create_line_plot(
    data=df,
    x="time",
    y="value",
    hue="category",
    title="Time Series",
    xlabel="Time",
    ylabel="Value",
    figsize=(12, 6),
    save_path="output/line_plot.png"
)

# Scatter plot
fig = plotter.create_scatter_plot(
    data=df,
    x="x_var",
    y="y_var",
    hue="group",
    size="size_var",
    title="Scatter Plot",
    figsize=(10, 8)
)

# Bar plot
fig = plotter.create_bar_plot(
    data=df,
    x="category",
    y="value",
    hue="subcategory",
    title="Bar Chart"
)

# Histogram
fig = plotter.create_histogram(
    data=df,
    column="value",
    hue="group",
    bins=30,
    title="Distribution"
)

# Box plot
fig = plotter.create_box_plot(
    data=df,
    x="category",
    y="value",
    hue="group",
    title="Box Plot"
)

# Heatmap
fig = plotter.create_heatmap(
    data=corr_matrix,
    annot=True,
    cmap="coolwarm",
    title="Correlation Heatmap"
)

# Correlation matrix
fig = plotter.create_correlation_matrix(
    data=df,
    method="pearson",
    annot=True,
    title="Correlation Matrix",
    save_path="output/correlation.png"
)
```

#### Helper Functions

```python
from scientific_template.plotting import create_figure, save_figure

# Create custom figure
fig, ax = create_figure(figsize=(10, 6), dpi=300)

# Save figure
save_figure(fig, "output/my_plot.pdf", dpi=300, bbox_inches='tight')
```

---

### Statistics Module

Provides common statistical analysis functions.

#### StatisticalAnalyzer - Statistical Analyzer

```python
from scientific_template.stats import StatisticalAnalyzer

analyzer = StatisticalAnalyzer()

# Descriptive statistics
stats = analyzer.descriptive_stats(df)
print(stats)

# Independent t-test
result = analyzer.ttest_independent(group1, group2, equal_var=True)
print(f"t={result['t_statistic']:.3f}, p={result['p_value']:.4f}")

# Paired t-test
result = analyzer.ttest_paired(before, after)

# One-way ANOVA
result = analyzer.anova_one_way(group1, group2, group3)
print(f"F={result['f_statistic']:.3f}, p={result['p_value']:.4f}")

# Chi-square test
result = analyzer.chi_square_test(observed_table)
print(f"χ²={result['chi_square']:.3f}, p={result['p_value']:.4f}")

# Correlation matrix
corr = analyzer.correlation(df, method="pearson")

# Pearson correlation
result = analyzer.pearson_correlation(x, y)
print(f"r={result['correlation']:.3f}, p={result['p_value']:.4f}")

# Spearman correlation
result = analyzer.spearman_correlation(x, y)

# Normality test
result = analyzer.normality_test(data, method="shapiro")
print(f"stat={result['statistic']:.3f}, p={result['p_value']:.4f}")

# Confidence interval
ci = analyzer.confidence_interval(data, confidence=0.95)
print(f"95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")
```

#### Convenience Functions

```python
from scientific_template.stats import perform_ttest, perform_anova

# t-test
result = perform_ttest(group1, group2, paired=False, equal_var=True)

# ANOVA
result = perform_anova(group1, group2, group3)
```

---

### Machine Learning Module

Provides simplified machine learning workflows.

#### ModelPipeline - Model Pipeline

```python
from scientific_template.ml import ModelPipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Initialize (includes feature scaling automatically)
pipeline = ModelPipeline(model=LinearRegression(), scaler=True)

# Train and evaluate
results = pipeline.fit(X, y, test_size=0.2, random_state=42)

# View results
print("Metrics:", results["metrics"])
# Regression: {'mse': ..., 'rmse': ..., 'r2': ...}
# Classification: {'accuracy': ..., 'precision': ..., 'recall': ..., 'f1': ...}

# Predict
predictions = pipeline.predict(X_new)

# Evaluate
metrics = pipeline.evaluate(X_test, y_test)
```

#### CrossValidator - Cross Validator

```python
from scientific_template.ml import CrossValidator
from sklearn.svm import SVC

cv = CrossValidator(cv=5)

# Cross-validation
results = cv.validate(
    model=SVC(),
    X=X,
    y=y,
    scoring="accuracy",
    shuffle=True,
    random_state=42
)

print(f"Mean Score: {results['mean_score']:.3f} ± {results['std_score']:.3f}")
print(f"Scores: {results['scores']}")
print(f"Range: [{results['min_score']:.3f}, {results['max_score']:.3f}]")

# Grid search
param_grid = {
    "C": [0.1, 1, 10],
    "kernel": ["linear", "rbf"]
}

grid_results = cv.grid_search(
    model=SVC(),
    X=X,
    y=y,
    param_grid=param_grid,
    scoring="accuracy"
)

print("Best Parameters:", grid_results["best_params"])
print("Best Score:", grid_results["best_score"])
```

---

### Utilities Module

General utility functions and helper features.

```python
from scientific_template.utils import (
    setup_logging,
    set_style,
    load_config,
    save_config,
    timer,
    get_timestamp,
    ensure_dir,
    flatten_dict,
    deep_merge
)

# Setup logging
logger = setup_logging(
    level="INFO",
    log_file="logs/app.log",
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger.info("Application started")

# Set plotting style
set_style(style="seaborn-v0_8", context="paper")

# Load configuration
config = load_config("config.yaml")
config = load_config("config.json")

# Save configuration
save_config({"key": "value"}, "output/config.yaml")

# Timer decorator
@timer
def slow_function():
    import time
    time.sleep(2)

slow_function()  # Output: slow_function completed in 2.00 s

# Get timestamp
timestamp = get_timestamp()  # "20240101_120000"
timestamp = get_timestamp("%Y-%m-%d %H:%M:%S")  # "2024-01-01 12:00:00"

# Ensure directory exists
data_dir = ensure_dir("data/output")

# Flatten nested dictionary
nested = {"a": {"b": 1, "c": 2}}
flat = flatten_dict(nested)  # {"a.b": 1, "a.c": 2}

# Deep merge dictionaries
dict1 = {"a": 1, "b": {"c": 2}}
dict2 = {"b": {"d": 3}, "e": 4}
merged = deep_merge(dict1, dict2)  # {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
```

---

## CLI Tool

After installation, use the `spt` command:

```bash
# Show help
spt --help

# Show version
spt --version

# Greeting command
spt hello --name "World"

# View data file info
spt info -i data/file.csv
spt info -i data/file.xlsx --format excel

# Configure plotting style
spt config-style --style seaborn-v0_8 --context paper

# Read configuration
spt config-get -c config.yaml
spt config-get -c config.yaml -k project.name

# Save configuration
spt config-save '{"key": "value"}' -o config.yaml

# Initialize new project
spt init
```

### Directory structure created by `spt init`

```
my_project/
├── data/           # Data directory
│   ├── input/      # Input data
│   └── output/     # Output data
├── notebooks/      # Jupyter notebooks
├── examples/       # Example code
├── tests/          # Test files
├── docs/           # Documentation
├── output/         # Analysis output
└── config.yaml     # Configuration file
```

---

## Configuration Management

### Configuration File Format

Supports YAML and JSON formats:

**config.yaml**:
```yaml
project:
  name: "My Analysis Project"
  version: "0.1.0"

data:
  input_dir: "data/input"
  output_dir: "data/output"

plotting:
  style: "seaborn-v0_8"
  context: "notebook"
  dpi: 300
  
logging:
  level: "INFO"
  file: "logs/app.log"

ml:
  test_size: 0.2
  random_state: 42
  cv_folds: 5
```

**config.json**:
```json
{
  "project": {
    "name": "My Analysis Project",
    "version": "0.1.0"
  },
  "plotting": {
    "style": "seaborn-v0_8",
    "dpi": 300
  }
}
```

### Using Configuration in Code

```python
from scientific_template.utils import load_config, set_style
import logging

# Load configuration
config = load_config("config.yaml")

# Apply configuration
set_style(
    style=config["plotting"]["style"],
    context=config["plotting"]["context"]
)

# Setup logging
logging.basicConfig(level=getattr(logging, config["logging"]["level"]))
```

---

## Best Practices

### 1. Project Structure

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── data_processing.py
│       └── analysis.py
├── data/
│   ├── raw/          # Raw data (unchanged)
│   ├── processed/    # Processed data
│   └── external/     # External data
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_modeling.ipynb
├── output/
│   ├── figures/      # Charts
│   ├── tables/       # Tables
│   └── models/       # Model files
├── tests/
├── config.yaml
├── pyproject.toml
└── README.md
```

### 2. Reproducibility

```python
# Always set random seed
import numpy as np
np.random.seed(42)

# Use random_state in model training
from scientific_template.ml import ModelPipeline
pipeline = ModelPipeline(model=..., scaler=True)
results = pipeline.fit(X, y, random_state=42)

# Record version information
from scientific_template import __version__
print(f"Using scientific-template v{__version__}")
```

### 3. Performance Optimization

```python
# Use polars for large datasets
loader = DataLoader(engine="polars")
df = loader.load_csv("large_file.csv")

# Use appropriate strategy for missing values
processor = DataProcessor()
df = processor.handle_missing(df, strategy="fill_mean")

# Process large files in batches
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)
```

### 4. Error Handling

```python
from scientific_template.data import DataLoader

loader = DataLoader()
try:
    df = loader.load("data/file.csv")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid file format: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Example Code

### Complete Analysis Workflow

```python
"""
Complete Data Analysis Example
"""
from scientific_template import (
    DataLoader, DataProcessor, DataCleaner, DataTransformer,
    Plotter, StatisticalAnalyzer, ModelPipeline, CrossValidator,
    setup_logging, load_config
)
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# 1. Initialize
logger = setup_logging(level="INFO", log_file="logs/analysis.log")
config = load_config("config.yaml")
logger.info("Starting analysis...")

# 2. Load data
loader = DataLoader(engine="pandas")
df = loader.load_csv("data/sales_data.csv")
logger.info(f"Loaded {len(df)} records")

# 3. Data cleaning
cleaner = DataCleaner()
df = cleaner.standardize_column_names(df)
df = cleaner.remove_whitespace(df)
df = cleaner.fix_data_types(df)

# 4. Data processing
processor = DataProcessor()
df = processor.remove_duplicates(df)
df = processor.handle_missing(df, strategy="fill_median")

# 5. Data transformation
transformer = DataTransformer()
df = transformer.normalize(df, method="zscore")
df = transformer.encode_categorical(df, method="onehot")

# 6. Exploratory analysis
analyzer = StatisticalAnalyzer()
desc_stats = analyzer.descriptive_stats(df)
print(desc_stats)

# Correlation analysis
corr = analyzer.correlation(df.select_dtypes(include=[np.number]))
print(corr)

# 7. Visualization
plotter = Plotter(style="seaborn-v0_8", context="notebook")

# Time series plot
fig = plotter.create_line_plot(
    df, x="date", y="sales",
    title="Sales Over Time",
    save_path="output/sales_trend.png"
)

# Distribution histogram
fig = plotter.create_histogram(
    df, column="sales",
    title="Sales Distribution",
    save_path="output/sales_dist.png"
)

# Correlation matrix heatmap
fig = plotter.create_correlation_matrix(
    df.select_dtypes(include=[np.number]),
    save_path="output/correlation.png"
)

# 8. Modeling
X = df.drop("target", axis=1)
y = df["target"]

pipeline = ModelPipeline(model=RandomForestRegressor(n_estimators=100))
results = pipeline.fit(X, y, test_size=0.2)

logger.info(f"Model R²: {results['metrics']['r2']:.3f}")
logger.info(f"Model RMSE: {results['metrics']['rmse']:.3f}")

# 9. Cross-validation
cv = CrossValidator(cv=5)
cv_results = cv.validate(
    model=RandomForestRegressor(n_estimators=100),
    X=X, y=y,
    scoring="r2"
)

logger.info(f"CV R²: {cv_results['mean_score']:.3f} ± {cv_results['std_score']:.3f}")

# 10. Complete
logger.info("Analysis complete!")
```

### Jupyter Notebook Example

```python
# notebook.ipynb

from scientific_template import *
import pandas as pd

# Quick setup
setup_logging()
Plotter.set_style("seaborn-v0_8", "notebook")

# Load data with one line
df = DataLoader().load_csv("data.csv")

# Quick statistics
StatisticalAnalyzer.descriptive_stats(df)

# Quick plotting
plotter = Plotter()
plotter.create_scatter_plot(df, "x", "y", hue="category")
```

---

## API Reference

### Class and Method Index

#### Data Module
- `DataLoader`
  - `load_csv()`, `load_excel()`, `load_json()`, `load_parquet()`, `load_feather()`
  - `load()` - Auto-detect format
- `DataProcessor`
  - `remove_duplicates()`, `handle_missing()`, `rename_columns()`
  - `select_columns()`, `filter_rows()`, `sort_values()`
  - `add_column()`, `get_info()`
- `DataCleaner`
  - `standardize_column_names()`, `remove_whitespace()`
  - `fix_data_types()`, `remove_special_characters()`
  - `validate_email()`, `detect_outliers_iqr()`, `clean_currency()`
- `DataTransformer`
  - `normalize()`, `encode_categorical()`
  - `pivot()`, `melt()`, `binning()`
  - `log_transform()`, `rolling_window()`

#### Plotting Module
- `Plotter`
  - `create_line_plot()`, `create_scatter_plot()`, `create_bar_plot()`
  - `create_histogram()`, `create_box_plot()`
  - `create_heatmap()`, `create_correlation_matrix()`
- `create_figure()`, `save_figure()`

#### Stats Module
- `StatisticalAnalyzer`
  - `descriptive_stats()`, `ttest_independent()`, `ttest_paired()`
  - `anova_one_way()`, `chi_square_test()`, `correlation()`
  - `pearson_correlation()`, `spearman_correlation()`
  - `normality_test()`, `confidence_interval()`
- `perform_ttest()`, `perform_anova()`

#### ML Module
- `ModelPipeline`
  - `fit()`, `predict()`, `evaluate()`
- `CrossValidator`
  - `validate()`, `grid_search()`

#### Utils Module
- `setup_logging()`, `set_style()`
- `load_config()`, `save_config()`
- `timer`, `get_timestamp()`, `ensure_dir()`
- `flatten_dict()`, `deep_merge()`

---

## Troubleshooting

### Common Issues

**Q: Polars import failed?**
A: Polars is an optional dependency. If not installed, it will automatically fall back to pandas. To use polars:
```bash
pip install polars
```

**Q: Chinese characters display incorrectly in charts?**
A: Set appropriate font:
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

**Q: Out of memory?**
A: Try using polars backend or chunk processing:
```python
loader = DataLoader(engine="polars")  # More memory efficient
# Or
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)
```

---

## Contributing

Welcome to submit Issues and Pull Requests!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## License

MIT License - see LICENSE file for details

---

## Contact

- Author: Your Name
- Email: your.email@example.com
- Project: https://github.com/yourusername/scientific-plotting-template
