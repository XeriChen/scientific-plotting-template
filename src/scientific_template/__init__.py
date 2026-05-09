"""
Scientific Plotting Template
==========================

A modern Python data analysis and visualization workspace.

This package provides a comprehensive set of tools for data analysis,
visualization, and statistical modeling, following best practices for
scientific computing and reproducible research.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from scientific_template.data import DataProcessor, DataLoader
from scientific_template.plotting import Plotter, create_figure, save_figure
from scientific_template.stats import StatisticalAnalyzer, perform_ttest, perform_anova
from scientific_template.utils import (
    setup_logging,
    set_style,
    load_config,
    save_config,
    timer,
)
from scientific_template.ml import ModelPipeline, CrossValidator

__all__ = [
    "DataProcessor",
    "DataLoader",
    "Plotter",
    "create_figure",
    "save_figure",
    "StatisticalAnalyzer",
    "perform_ttest",
    "perform_anova",
    "setup_logging",
    "set_style",
    "load_config",
    "save_config",
    "timer",
    "ModelPipeline",
    "CrossValidator",
]