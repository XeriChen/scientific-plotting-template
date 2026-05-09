"""
Plotting Module
===============

Visualization tools for scientific data analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Union, List, Dict, Any, Tuple
from pathlib import Path
import pandas as pd


class Plotter:
    """
    A comprehensive plotting utility for creating publication-quality visualizations.
    
    Supports matplotlib, seaborn, and plotly backends.
    """
    
    def __init__(self, style: str = "seaborn-v0_8", context: str = "notebook"):
        """
        Initialize the Plotter.
        
        Args:
            style: Matplotlib/seaborn style name
            context: Context for parameter scaling
        """
        self.style = style
        self.context = context
        self.set_style(style, context)
    
    @staticmethod
    def set_style(style: str = "seaborn-v0_8", context: str = "notebook"):
        """Set plotting style."""
        sns.set_style(style)
        sns.set_context(context)
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['savefig.dpi'] = 300
    
    def create_line_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        title: str = "",
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a line plot."""
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue:
            for value in data[hue].unique():
                subset = data[data[hue] == value]
                ax.plot(subset[x], subset[y], label=value)
            ax.legend()
        else:
            ax.plot(data[x], data[y])
        
        ax.set_title(title)
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel or y)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_scatter_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        size: Optional[str] = None,
        title: str = "",
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a scatter plot."""
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue:
            for value in data[hue].unique():
                subset = data[data[hue] == value]
                ax.scatter(subset[x], subset[y], label=value, alpha=0.7)
            ax.legend()
        else:
            ax.scatter(data[x], data[y], alpha=0.7)
        
        ax.set_title(title)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_bar_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        title: str = "",
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a bar plot."""
        fig, ax = plt.subplots(figsize=figsize)
        sns.barplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_histogram(
        self,
        data: pd.DataFrame,
        column: str,
        hue: Optional[str] = None,
        bins: int = 30,
        title: str = "",
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a histogram."""
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue:
            for value in data[hue].unique():
                subset = data[data[hue] == value]
                ax.hist(subset[column], bins=bins, label=value, alpha=0.7)
            ax.legend()
        else:
            ax.hist(data[column], bins=bins, alpha=0.7)
        
        ax.set_title(title)
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_box_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        title: str = "",
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a box plot."""
        fig, ax = plt.subplots(figsize=figsize)
        sns.boxplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_heatmap(
        self,
        data: pd.DataFrame,
        annot: bool = True,
        cmap: str = "coolwarm",
        title: str = "",
        figsize: Tuple[int, int] = (10, 8),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a heatmap."""
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(data, annot=annot, cmap=cmap, ax=ax)
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_correlation_matrix(
        self,
        data: pd.DataFrame,
        method: str = "pearson",
        annot: bool = True,
        cmap: str = "coolwarm",
        title: str = "Correlation Matrix",
        figsize: Tuple[int, int] = (12, 10),
        save_path: Optional[Union[str, Path]] = None
    ) -> plt.Figure:
        """Create a correlation matrix heatmap."""
        corr = data.corr(method=method)
        return self.create_heatmap(corr, annot, cmap, title, figsize, save_path)


def create_figure(figsize: Tuple[int, int] = (10, 6), dpi: int = 100) -> Tuple[plt.Figure, plt.Axes]:
    """Create a new figure with specified parameters."""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    return fig, ax


def save_figure(fig: plt.Figure, path: Union[str, Path], dpi: int = 300, **kwargs):
    """Save a figure to file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches='tight', **kwargs)