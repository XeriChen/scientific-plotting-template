"""
Data Loader Module
==================

Utilities for loading data from various file formats.
"""

import pandas as pd
from pathlib import Path
from typing import Union, Optional, Dict, Any, TYPE_CHECKING

# Try to import polars, but make it optional
try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    pl = None  # type: ignore

# For type hints only when polars is not installed
if TYPE_CHECKING:
    import pandas as pd
    try:
        import polars as pl
    except ImportError:
        pass

DataFrame = Union[pd.DataFrame, "pl.DataFrame"] if HAS_POLARS else pd.DataFrame


class DataLoader:
    """
    A versatile data loader supporting multiple file formats.
    
    Supports: CSV, Excel, JSON, Parquet, Feather, and more.
    """
    
    def __init__(self, engine: str = "pandas"):
        """
        Initialize the DataLoader.
        
        Args:
            engine: Backend engine to use ("pandas" or "polars")
        """
        if engine not in ["pandas", "polars"]:
            raise ValueError("Engine must be 'pandas' or 'polars'")
        self.engine = engine
    
    def load_csv(
        self, 
        filepath: Union[str, Path], 
        **kwargs
    ) -> DataFrame:
        """
        Load data from a CSV file.
        
        Args:
            filepath: Path to the CSV file
            **kwargs: Additional arguments passed to the reader
            
        Returns:
            DataFrame containing the loaded data
        """
        filepath = Path(filepath)
        if self.engine == "pandas":
            return pd.read_csv(filepath, **kwargs)
        else:
            return pl.read_csv(filepath, **kwargs)
    
    def load_excel(
        self,
        filepath: Union[str, Path],
        sheet_name: Optional[Union[int, str]] = None,
        **kwargs
    ) -> Union[DataFrame, Dict[str, pd.DataFrame]]:
        """
        Load data from an Excel file.
        
        Args:
            filepath: Path to the Excel file
            sheet_name: Sheet name or index to load (None for all sheets)
            **kwargs: Additional arguments passed to the reader
            
        Returns:
            DataFrame or dict of DataFrames
        """
        filepath = Path(filepath)
        if self.engine == "pandas":
            return pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
        else:
            # Polars reads only one sheet at a time
            return pl.read_excel(filepath, sheet_name=sheet_name, **kwargs)
    
    def load_json(
        self,
        filepath: Union[str, Path],
        **kwargs
    ) -> DataFrame:
        """
        Load data from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            **kwargs: Additional arguments passed to the reader
            
        Returns:
            DataFrame containing the loaded data
        """
        filepath = Path(filepath)
        if self.engine == "pandas":
            return pd.read_json(filepath, **kwargs)
        else:
            return pl.read_json(filepath, **kwargs)
    
    def load_parquet(
        self,
        filepath: Union[str, Path],
        **kwargs
    ) -> DataFrame:
        """
        Load data from a Parquet file.
        
        Args:
            filepath: Path to the Parquet file
            **kwargs: Additional arguments passed to the reader
            
        Returns:
            DataFrame containing the loaded data
        """
        filepath = Path(filepath)
        if self.engine == "pandas":
            return pd.read_parquet(filepath, **kwargs)
        else:
            return pl.read_parquet(filepath, **kwargs)
    
    def load_feather(
        self,
        filepath: Union[str, Path],
        **kwargs
    ) -> DataFrame:
        """
        Load data from a Feather file.
        
        Args:
            filepath: Path to the Feather file
            **kwargs: Additional arguments passed to the reader
            
        Returns:
            DataFrame containing the loaded data
        """
        filepath = Path(filepath)
        if self.engine == "pandas":
            return pd.read_feather(filepath, **kwargs)
        else:
            return pl.read_ipc(filepath, **kwargs)
    
    def load(
        self,
        filepath: Union[str, Path],
        file_format: Optional[str] = None,
        **kwargs
    ) -> DataFrame:
        """
        Auto-detect file format and load data.
        
        Args:
            filepath: Path to the data file
            file_format: Explicit format specification (optional)
            **kwargs: Additional arguments passed to the reader
            
        Returns:
            DataFrame containing the loaded data
        """
        filepath = Path(filepath)
        
        if file_format is None:
            suffix = filepath.suffix.lower()
            format_map = {
                '.csv': 'csv',
                '.tsv': 'csv',
                '.xlsx': 'excel',
                '.xls': 'excel',
                '.json': 'json',
                '.parquet': 'parquet',
                '.feather': 'feather',
                '.ipc': 'feather',
            }
            file_format = format_map.get(suffix)
        
        if file_format is None:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        loaders = {
            'csv': self.load_csv,
            'excel': self.load_excel,
            'json': self.load_json,
            'parquet': self.load_parquet,
            'feather': self.load_feather,
        }
        
        return loaders[file_format](filepath, **kwargs)
