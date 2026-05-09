"""
Data Cleaning Module
====================

Utilities for cleaning and validating data.
"""

import pandas as pd
# Try to import polars, but make it optional
try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    class _DummyPolars:
        DataFrame = None  # type: ignore
    pl = _DummyPolars()  # type: ignore
from typing import Union, Optional, List, Dict, Any, Set
import re


class DataCleaner:
    """
    A comprehensive data cleaning utility for handling common data quality issues.
    
    Supports both pandas and polars backends.
    """
    
    def __init__(self, engine: str = "pandas"):
        """
        Initialize the DataCleaner.
        
        Args:
            engine: Backend engine to use ("pandas" or "polars")
        """
        if engine not in ["pandas", "polars"]:
            raise ValueError("Engine must be 'pandas' or 'polars'")
        self.engine = engine
    
    def standardize_column_names(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        case: str = "snake"
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Standardize column names to a consistent format.
        
        Args:
            df: Input DataFrame
            case: Target case format ("snake", "lower", "upper")
            
        Returns:
            DataFrame with standardized column names
        """
        if self.engine == "pandas":
            columns = df.columns.tolist()
        else:
            columns = df.columns
        
        new_names = {}
        for col in columns:
            new_name = col.strip()
            # Replace spaces and special chars with underscores
            new_name = re.sub(r'[^a-zA-Z0-9]', '_', new_name)
            # Remove consecutive underscores
            new_name = re.sub(r'_+', '_', new_name)
            # Remove leading/trailing underscores
            new_name = new_name.strip('_')
            
            if case == "snake":
                new_name = new_name.lower()
            elif case == "lower":
                new_name = new_name.lower()
            elif case == "upper":
                new_name = new_name.upper()
            
            new_names[col] = new_name
        
        if self.engine == "pandas":
            return df.rename(columns=new_names)
        else:
            return df.rename(new_names)
    
    def remove_whitespace(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        columns: Optional[List[str]] = None
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Remove leading and trailing whitespace from string columns.
        
        Args:
            df: Input DataFrame
            columns: Specific columns to process (None for all string columns)
            
        Returns:
            DataFrame with trimmed strings
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.select_dtypes(include=['object', 'string']).columns.tolist()
            
            for col in columns:
                if df[col].dtype == object:
                    df[col] = df[col].str.strip()
            return df
        else:
            if columns is None:
                # Get string columns
                columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if str(dtype) in ['String', 'Utf8']]
            
            for col in columns:
                df = df.with_columns(pl.col(col).str.strip_chars())
            return df
    
    def fix_data_types(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        column_types: Optional[Dict[str, str]] = None
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Fix data types for columns.
        
        Args:
            df: Input DataFrame
            column_types: Dictionary mapping column names to target types
            
        Returns:
            DataFrame with corrected data types
        """
        if self.engine == "pandas":
            if column_types:
                df = df.astype(column_types)
            # Try to convert numeric columns
            for col in df.columns:
                if df[col].dtype == object:
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except (ValueError, TypeError):
                        pass
            return df
        else:
            if column_types:
                type_map = {
                    'int': pl.Int64,
                    'float': pl.Float64,
                    'str': pl.String,
                    'bool': pl.Boolean,
                    'datetime': pl.Datetime,
                }
                for col, dtype in column_types.items():
                    df = df.with_columns(pl.col(col).cast(type_map.get(dtype, pl.String)))
            return df
    
    def remove_special_characters(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        columns: Optional[List[str]] = None,
        pattern: str = r'[^a-zA-Z0-9\s]'
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Remove special characters from string columns.
        
        Args:
            df: Input DataFrame
            columns: Specific columns to process (None for all string columns)
            pattern: Regex pattern for characters to remove
            
        Returns:
            DataFrame with cleaned strings
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.select_dtypes(include=['object', 'string']).columns.tolist()
            
            for col in columns:
                if df[col].dtype == object:
                    df[col] = df[col].str.replace(pattern, '', regex=True)
            return df
        else:
            if columns is None:
                columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if str(dtype) in ['String', 'Utf8']]
            
            for col in columns:
                df = df.with_columns(pl.col(col).str.replace_all(pattern, ''))
            return df
    
    def validate_email(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        column: str,
        remove_invalid: bool = True
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Validate and optionally remove invalid email addresses.
        
        Args:
            df: Input DataFrame
            column: Column containing email addresses
            remove_invalid: Whether to remove rows with invalid emails
            
        Returns:
            DataFrame with validated emails
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if self.engine == "pandas":
            mask = df[column].astype(str).str.match(email_pattern, na=False)
            if remove_invalid:
                return df[mask]
            else:
                df[f'{column}_valid'] = mask
                return df
        else:
            mask = pl.col(column).cast(pl.String).str.contains(email_pattern)
            if remove_invalid:
                return df.filter(mask)
            else:
                return df.with_columns(mask.alias(f'{column}_valid'))
    
    def detect_outliers_iqr(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        columns: Optional[List[str]] = None,
        multiplier: float = 1.5
    ) -> Union[pd.DataFrame, Dict[str, pd.Series]]:
        """
        Detect outliers using the IQR method.
        
        Args:
            df: Input DataFrame
            columns: Numeric columns to check (None for all numeric)
            multiplier: IQR multiplier for outlier threshold
            
        Returns:
            DataFrame with boolean outlier flags or dict of outlier masks
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.select_dtypes(include=['number']).columns.tolist()
            
            outlier_flags = {}
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
                outlier_flags[col] = (df[col] < lower_bound) | (df[col] > upper_bound)
            
            return outlier_flags
        else:
            if columns is None:
                columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if str(dtype) in ['Int64', 'Float64', 'Int32', 'Float32']]
            
            outlier_flags = {}
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
                outlier_flags[col] = df.select(
                    ((pl.col(col) < lower_bound) | (pl.col(col) > upper_bound)).alias(col)
                )[col]
            
            return outlier_flags
    
    def clean_currency(
        self,
        df: Union[pd.DataFrame, pl.DataFrame],
        columns: Optional[List[str]] = None
    ) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Clean currency columns by removing symbols and converting to numeric.
        
        Args:
            df: Input DataFrame
            columns: Columns to clean (None for auto-detection)
            
        Returns:
            DataFrame with cleaned currency columns
        """
        if self.engine == "pandas":
            if columns is None:
                columns = []
                for col in df.columns:
                    if df[col].dtype == object:
                        sample = str(df[col].iloc[0]) if len(df) > 0 else ""
                        if any(sym in sample for sym in ['$', '€', '£', '¥']):
                            columns.append(col)
            
            for col in columns:
                df[col] = df[col].astype(str).str.replace(r'[,$€£¥\s]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        else:
            # For polars, user should specify columns
            if columns is None:
                return df
            
            for col in columns:
                df = df.with_columns(
                    pl.col(col)
                    .cast(pl.String)
                    .str.replace_all(r'[$€£¥,\s]', '')
                    .cast(pl.Float64, strict=False)
                )
            
            return df
