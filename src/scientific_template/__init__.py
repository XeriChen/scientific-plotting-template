"""
Scientific Plotting Template
==========================

A modern Python data analysis and visualization workspace.

This package provides a comprehensive set of tools for data analysis,
visualization, and statistical modeling, following best practices for
scientific computing and reproducible research.

## Quick Start

```python
from scientific_template import *

# Load and analyze data
df = DataLoader().load_csv("data.csv")
stats = StatisticalAnalyzer.descriptive_stats(df)

# Create visualizations
plotter = Plotter()
fig = plotter.create_histogram(df, column="value")
plotter.save_figure(fig, "output/plot.png")

# Build ML models
pipeline = ModelPipeline(model=RandomForestClassifier())
results = pipeline.fit(X, y)
```

## Modules

- **data**: Data loading, cleaning, processing, and transformation
- **plotting**: Publication-quality visualizations
- **stats**: Statistical analysis and hypothesis testing
- **ml**: Machine learning utilities and pipelines
- **utils**: General utilities (logging, configuration, timing)
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Data processing modules
from scientific_template.data import (
    DataLoader,
    DataProcessor,
    DataCleaner,
    DataTransformer,
)

# Visualization modules
from scientific_template.plotting import (
    Plotter,
    create_figure,
    save_figure,
)

# Statistical analysis modules
from scientific_template.stats import (
    StatisticalAnalyzer,
    perform_ttest,
    perform_anova,
)

# Machine learning modules
from scientific_template.ml import (
    ModelPipeline,
    CrossValidator,
)

# Utility functions
from scientific_template.utils import (
    setup_logging,
    set_style,
    load_config,
    save_config,
    timer,
    get_timestamp,
    ensure_dir,
    flatten_dict,
    deep_merge,
)

__all__ = [
    # Data processing
    "DataLoader",
    "DataProcessor",
    "DataCleaner",
    "DataTransformer",
    
    # Visualization
    "Plotter",
    "create_figure",
    "save_figure",
    
    # Statistics
    "StatisticalAnalyzer",
    "perform_ttest",
    "perform_anova",
    
    # Machine learning
    "ModelPipeline",
    "CrossValidator",
    
    # Utilities
    "setup_logging",
    "set_style",
    "load_config",
    "save_config",
    "timer",
    "get_timestamp",
    "ensure_dir",
    "flatten_dict",
    "deep_merge",
]