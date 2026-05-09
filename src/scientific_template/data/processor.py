"""
Data Processor Module
=====================

Utilities for processing and manipulating data.
"""

import pandas as pd
from typing import Union, Optional, List, Dict, Any, TYPE_CHECKING, Callable
from pathlib import Path

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


class DataProcessor:
    """
    A comprehensive data processor for cleaning, transforming, and preparing data.
    
    Supports both pandas and polars backends.
    """
    
    def __init__(self, engine: str = "pandas"):
        """
        Initialize the DataProcessor.
        
        Args:
            engine: Backend engine to use ("pandas" or "polars")
        """
        if engine not in ["pandas", "polars"]:
            raise ValueError("Engine must be 'pandas' or 'polars'")
        self.engine = engine
    
    def remove_duplicates(
        self,
        df: DataFrame,
        subset: Optional[List[str]] = None,
        keep: str = "first"
    ) -> DataFrame:
        """
        Remove duplicate rows from the DataFrame.
        
        Args:
            df: Input DataFrame
            subset: Columns to consider for duplicates
            keep: Which duplicate to keep ("first", "last", False)
            
        Returns:
            DataFrame with duplicates removed
        """
        if self.engine == "pandas":
            return df.drop_duplicates(subset=subset, keep=keep)
        else:
            if subset is None:
                return df.unique()
            else:
                return df.unique(subset=subset, keep=keep)
    
    def handle_missing(
        self,
        df: DataFrame,
        strategy: str = "drop",
        columns: Optional[List[str]] = None,
        fill_value: Any = None
    ) -> DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            df: Input DataFrame
            strategy: Strategy for handling missing values ("drop", "fill_mean", 
                     "fill_median", "fill_mode", "fill_value")
            columns: Specific columns to process (None for all)
            fill_value: Value to use when strategy is "fill_value"
            
        Returns:
            DataFrame with missing values handled
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.columns.tolist()
            
            if strategy == "drop":
                return df.dropna(subset=columns)
            elif strategy == "fill_mean":
                df[columns] = df[columns].fillna(df[columns].mean())
                return df
            elif strategy == "fill_median":
                df[columns] = df[columns].fillna(df[columns].median())
                return df
            elif strategy == "fill_mode":
                for col in columns:
                    df[col] = df[col].fillna(df[col].mode()[0])
                return df
            elif strategy == "fill_value":
                df[columns] = df[columns].fillna(fill_value)
                return df
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
        else:
            if columns is None:
                columns = df.columns
            
            if strategy == "drop":
                return df.drop_nulls(subset=columns)
            elif strategy == "fill_mean":
                for col in columns:
                    df = df.with_columns(pl.col(col).fill_null(pl.col(col).mean()))
                return df
            elif strategy == "fill_median":
                # Polars doesn't have direct median fill, approximate
                for col in columns:
                    median_val = df[col].median()
                    df = df.with_columns(pl.col(col).fill_null(median_val))
                return df
            elif strategy == "fill_value":
                for col in columns:
                    df = df.with_columns(pl.col(col).fill_null(fill_value))
                return df
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
    
    def rename_columns(
        self,
        df: DataFrame,
        mapping: Dict[str, str]
    ) -> DataFrame:
        """
        Rename columns in the DataFrame.
        
        Args:
            df: Input DataFrame
            mapping: Dictionary mapping old names to new names
            
        Returns:
            DataFrame with renamed columns
        """
        if self.engine == "pandas":
            return df.rename(columns=mapping)
        else:
            return df.rename(mapping)
    
    def select_columns(
        self,
        df: DataFrame,
        columns: List[str]
    ) -> DataFrame:
        """
        Select specific columns from the DataFrame.
        
        Args:
            df: Input DataFrame
            columns: List of column names to select
            
        Returns:
            DataFrame with selected columns only
        """
        if self.engine == "pandas":
            return df[columns]
        else:
            return df.select(columns)
    
    def filter_rows(
        self,
        df: DataFrame,
        condition: Callable[[Any], bool]
    ) -> DataFrame:
        """
        Filter rows based on a condition.
        
        Args:
            df: Input DataFrame
            condition: Function that returns True for rows to keep
            
        Returns:
            Filtered DataFrame
        """
        if self.engine == "pandas":
            return df[condition(df)]
        else:
            # For polars, condition should be a polars expression
            return df.filter(condition)
    
    def sort_values(
        self,
        df: DataFrame,
        by: Union[str, List[str]],
        ascending: Union[bool, List[bool]] = True
    ) -> DataFrame:
        """
        Sort DataFrame by values.
        
        Args:
            df: Input DataFrame
            by: Column name(s) to sort by
            ascending: Sort order(s)
            
        Returns:
            Sorted DataFrame
        """
        if self.engine == "pandas":
            return df.sort_values(by=by, ascending=ascending)
        else:
            if isinstance(by, str):
                by = [by]
            if isinstance(ascending, bool):
                ascending = [ascending] * len(by)
            return df.sort(by=by, descending=[not a for a in ascending])
    
    def add_column(
        self,
        df: DataFrame,
        name: str,
        values: Union[Any, List[Any], Callable]
    ) -> DataFrame:
        """
        Add a new column to the DataFrame.
        
        Args:
            df: Input DataFrame
            name: Name of the new column
            values: Values to add (scalar, list, or function)
            
        Returns:
            DataFrame with new column added
        """
        if self.engine == "pandas":
            if callable(values):
                df[name] = df.apply(values, axis=1)
            else:
                df[name] = values
            return df
        else:
            if callable(values):
                # For polars, apply function to each row
                df = df.with_columns(pl.struct(df.columns).map_elements(values).alias(name))
            else:
                df = df.with_columns(pl.lit(values).alias(name))
            return df
    
    def get_info(self, df: DataFrame) -> Dict[str, Any]:
        """
        Get summary information about the DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with DataFrame information
        """
        if self.engine == "pandas":
            return {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
            }
        else:
            return {
                "shape": df.shape,
                "columns": df.columns,
                "dtypes": {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)},
                "null_counts": {col: df[col].null_count() for col in df.columns},
            }
