"""
Data Transform Module
=====================

Utilities for transforming and reshaping data.
"""

import pandas as pd
from typing import Union, Optional, List, Dict, Any, TYPE_CHECKING, Callable
import numpy as np

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


class DataTransformer:
    """
    A comprehensive data transformation utility for reshaping and modifying data.
    
    Supports both pandas and polars backends.
    """
    
    def __init__(self, engine: str = "pandas"):
        """
        Initialize the DataTransformer.
        
        Args:
            engine: Backend engine to use ("pandas" or "polars")
        """
        if engine not in ["pandas", "polars"]:
            raise ValueError("Engine must be 'pandas' or 'polars'")
        self.engine = engine
    
    def normalize(
        self,
        df: DataFrame,
        columns: Optional[List[str]] = None,
        method: str = "minmax"
    ) -> DataFrame:
        """
        Normalize numeric columns.
        
        Args:
            df: Input DataFrame
            columns: Columns to normalize (None for all numeric)
            method: Normalization method ("minmax", "zscore", "robust")
            
        Returns:
            DataFrame with normalized columns
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.select_dtypes(include=['number']).columns.tolist()
            
            result = df.copy()
            for col in columns:
                if method == "minmax":
                    min_val = result[col].min()
                    max_val = result[col].max()
                    if max_val - min_val != 0:
                        result[col] = (result[col] - min_val) / (max_val - min_val)
                    else:
                        result[col] = 0
                elif method == "zscore":
                    mean = result[col].mean()
                    std = result[col].std()
                    if std != 0:
                        result[col] = (result[col] - mean) / std
                    else:
                        result[col] = 0
                elif method == "robust":
                    median = result[col].median()
                    q1 = result[col].quantile(0.25)
                    q3 = result[col].quantile(0.75)
                    iqr = q3 - q1
                    if iqr != 0:
                        result[col] = (result[col] - median) / iqr
                    else:
                        result[col] = 0
            return result
        else:
            if columns is None:
                columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if str(dtype) in ['Int64', 'Float64', 'Int32', 'Float32']]
            
            result = df.clone()
            for col in columns:
                if method == "minmax":
                    min_val = result[col].min()
                    max_val = result[col].max()
                    if max_val - min_val != 0:
                        result = result.with_columns(
                            ((pl.col(col) - min_val) / (max_val - min_val)).alias(col)
                        )
                    else:
                        result = result.with_columns(pl.lit(0).alias(col))
                elif method == "zscore":
                    mean = result[col].mean()
                    std = result[col].std()
                    if std != 0:
                        result = result.with_columns(
                            ((pl.col(col) - mean) / std).alias(col)
                        )
                    else:
                        result = result.with_columns(pl.lit(0).alias(col))
            return result
    
    def encode_categorical(
        self,
        df: DataFrame,
        columns: Optional[List[str]] = None,
        method: str = "onehot"
    ) -> DataFrame:
        """
        Encode categorical variables.
        
        Args:
            df: Input DataFrame
            columns: Columns to encode (None for all object/string columns)
            method: Encoding method ("onehot", "label", "frequency")
            
        Returns:
            DataFrame with encoded columns
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            result = df.copy()
            if method == "onehot":
                result = pd.get_dummies(result, columns=columns, drop_first=True)
            elif method == "label":
                from sklearn.preprocessing import LabelEncoder
                for col in columns:
                    le = LabelEncoder()
                    result[col] = le.fit_transform(result[col].astype(str))
            elif method == "frequency":
                for col in columns:
                    freq_map = result[col].value_counts().to_dict()
                    result[col] = result[col].map(freq_map)
            return result
        else:
            if columns is None:
                columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if str(dtype) in ['String', 'Utf8', 'Categorical']]
            
            result = df.clone()
            if method == "onehot":
                result = result.to_dummies(columns=columns, drop_first=True)
            elif method == "label":
                for col in columns:
                    categories = result[col].unique().sort()
                    cat_map = {cat: idx for idx, cat in enumerate(categories)}
                    result = result.with_columns(
                        pl.col(col).replace(cat_map).alias(col)
                    )
            elif method == "frequency":
                for col in columns:
                    freq_map = dict(result[col].value_counts().rows())
                    result = result.with_columns(
                        pl.col(col).replace(freq_map).alias(col)
                    )
            return result
    
    def pivot(
        self,
        df: DataFrame,
        index: str,
        columns: str,
        values: str,
        aggfunc: str = "mean"
    ) -> DataFrame:
        """
        Pivot the DataFrame.
        
        Args:
            df: Input DataFrame
            index: Column to use as index
            columns: Column to use for new columns
            values: Column to use for values
            aggfunc: Aggregation function ("mean", "sum", "count", etc.)
            
        Returns:
            Pivoted DataFrame
        """
        if self.engine == "pandas":
            return df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)
        else:
            return df.pivot(index=index, columns=columns, values=values, aggregate_function=aggfunc)
    
    def melt(
        self,
        df: DataFrame,
        id_vars: Optional[List[str]] = None,
        value_vars: Optional[List[str]] = None,
        var_name: str = "variable",
        value_name: str = "value"
    ) -> DataFrame:
        """
        Melt the DataFrame from wide to long format.
        
        Args:
            df: Input DataFrame
            id_vars: Columns to keep as identifiers
            value_vars: Columns to unpivot (None for all non-id columns)
            var_name: Name for the variable column
            value_name: Name for the value column
            
        Returns:
            Melted DataFrame
        """
        if self.engine == "pandas":
            return pd.melt(
                df, 
                id_vars=id_vars, 
                value_vars=value_vars,
                var_name=var_name, 
                value_name=value_name
            )
        else:
            return df.melt(
                id_vars=id_vars,
                value_vars=value_vars,
                variable_name=var_name,
                value_name=value_name
            )
    
    def binning(
        self,
        df: DataFrame,
        column: str,
        bins: Union[int, List[float]],
        labels: Optional[List[str]] = None,
        right: bool = True
    ) -> DataFrame:
        """
        Bin continuous data into discrete intervals.
        
        Args:
            df: Input DataFrame
            column: Column to bin
            bins: Number of bins or bin edges
            labels: Labels for the bins (optional)
            right: Whether bins include the right edge
            
        Returns:
            DataFrame with binned column added
        """
        if self.engine == "pandas":
            df[f'{column}_binned'] = pd.cut(
                df[column], 
                bins=bins, 
                labels=labels,
                right=right
            )
            return df
        else:
            if isinstance(bins, int):
                # Create equal-width bins
                min_val = df[column].min()
                max_val = df[column].max()
                step = (max_val - min_val) / bins
                bin_edges = [min_val + i * step for i in range(bins + 1)]
            else:
                bin_edges = bins
            
            # Use cut function from polars
            df = df.with_columns(
                pl.col(column).cut(bin_edges, label_mode="left").alias(f'{column}_binned')
            )
            return df
    
    def log_transform(
        self,
        df: DataFrame,
        columns: Optional[List[str]] = None,
        base: float = np.e
    ) -> DataFrame:
        """
        Apply log transformation to numeric columns.
        
        Args:
            df: Input DataFrame
            columns: Columns to transform (None for all numeric)
            base: Logarithm base (e for natural log, 10 for common log, 2 for binary)
            
        Returns:
            DataFrame with transformed columns
        """
        if self.engine == "pandas":
            if columns is None:
                columns = df.select_dtypes(include=['number']).columns.tolist()
            
            result = df.copy()
            for col in columns:
                if base == np.e:
                    result[col] = np.log1p(result[col])  # log(1 + x) to handle zeros
                elif base == 10:
                    result[col] = np.log10(result[col] + 1)
                elif base == 2:
                    result[col] = np.log2(result[col] + 1)
            return result
        else:
            if columns is None:
                columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if str(dtype) in ['Int64', 'Float64', 'Int32', 'Float32']]
            
            result = df.clone()
            for col in columns:
                if base == np.e:
                    result = result.with_columns(
                        pl.col(col).log().alias(col)
                    )
                elif base == 10:
                    result = result.with_columns(
                        (pl.col(col) + 1).log(10).alias(col)
                    )
                elif base == 2:
                    result = result.with_columns(
                        (pl.col(col) + 1).log(2).alias(col)
                    )
            return result
    
    def rolling_window(
        self,
        df: DataFrame,
        column: str,
        window: int,
        operation: str = "mean",
        min_periods: Optional[int] = None
    ) -> pd.Series:
        """
        Apply rolling window operations.
        
        Args:
            df: Input DataFrame
            column: Column to apply rolling window
            window: Window size
            operation: Operation to apply ("mean", "sum", "std", "min", "max")
            min_periods: Minimum number of observations required
            
        Returns:
            Series with rolling window results
        """
        if self.engine == "pandas":
            roller = df[column].rolling(window=window, min_periods=min_periods or window)
            if operation == "mean":
                return roller.mean()
            elif operation == "sum":
                return roller.sum()
            elif operation == "std":
                return roller.std()
            elif operation == "min":
                return roller.min()
            elif operation == "max":
                return roller.max()
        else:
            if min_periods is None:
                min_periods = window
            
            if operation == "mean":
                return df[column].rolling_mean(window_size=window, min_periods=min_periods)
            elif operation == "sum":
                return df[column].rolling_sum(window_size=window, min_periods=min_periods)
            elif operation == "std":
                return df[column].rolling_std(window_size=window, min_periods=min_periods)
            elif operation == "min":
                return df[column].rolling_min(window_size=window, min_periods=min_periods)
            elif operation == "max":
                return df[column].rolling_max(window_size=window, min_periods=min_periods)
