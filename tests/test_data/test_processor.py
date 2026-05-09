"""
Tests for the data processor module.
"""
import pytest
import pandas as pd
import numpy as np
from scientific_template.data.processor import DataProcessor


class TestDataProcessor:
    """Test cases for DataProcessor class."""
    
    def test_init_default(self):
        """Test default initialization."""
        processor = DataProcessor()
        assert processor.engine == "pandas"
    
    def test_remove_duplicates(self, df_with_duplicates):
        """Test removing duplicates."""
        processor = DataProcessor()
        df_clean = processor.remove_duplicates(df_with_duplicates)
        
        assert len(df_clean) == 4  # Should remove 2 duplicates
    
    def test_remove_duplicates_subset(self, df_with_duplicates):
        """Test removing duplicates with subset."""
        processor = DataProcessor()
        df_clean = processor.remove_duplicates(df_with_duplicates, subset=['id'])
        
        assert len(df_clean) == 4
    
    def test_handle_missing_drop(self, df_with_missing):
        """Test handling missing values by dropping."""
        processor = DataProcessor()
        df_clean = processor.handle_missing(df_with_missing, strategy="drop")
        
        assert len(df_clean) == 3  # Only rows without NaN
    
    def test_handle_missing_fill_mean(self, df_with_missing):
        """Test handling missing values with mean."""
        processor = DataProcessor()
        df_clean = processor.handle_missing(
            df_with_missing, 
            strategy="fill_mean",
            columns=['a', 'b']
        )
        
        assert df_clean['a'].isnull().sum() == 0
        assert df_clean['b'].isnull().sum() == 0
    
    def test_rename_columns(self, sample_df):
        """Test renaming columns."""
        processor = DataProcessor()
        mapping = {'name': 'full_name', 'age': 'years'}
        df_renamed = processor.rename_columns(sample_df, mapping)
        
        assert 'full_name' in df_renamed.columns
        assert 'years' in df_renamed.columns
        assert 'name' not in df_renamed.columns
        assert 'age' not in df_renamed.columns
    
    def test_select_columns(self, sample_df):
        """Test selecting specific columns."""
        processor = DataProcessor()
        df_selected = processor.select_columns(sample_df, ['id', 'name'])
        
        assert df_selected.shape == (5, 2)
        assert list(df_selected.columns) == ['id', 'name']
    
    def test_sort_values(self, sample_df):
        """Test sorting values."""
        processor = DataProcessor()
        df_sorted = processor.sort_values(sample_df, by='age', ascending=False)
        
        assert df_sorted.iloc[0]['age'] == 45
        assert df_sorted.iloc[-1]['age'] == 25
    
    def test_add_column_scalar(self, sample_df):
        """Test adding column with scalar value."""
        processor = DataProcessor()
        df_new = processor.add_column(sample_df, 'constant', 100)
        
        assert 'constant' in df_new.columns
        assert (df_new['constant'] == 100).all()
    
    def test_get_info(self, sample_df):
        """Test getting DataFrame info."""
        processor = DataProcessor()
        info = processor.get_info(sample_df)
        
        assert info['shape'] == (5, 6)
        assert 'columns' in info
        assert 'dtypes' in info
