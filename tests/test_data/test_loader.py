"""
Tests for the data loader module.
"""
import pytest
import pandas as pd
from pathlib import Path
from scientific_template.data.loader import DataLoader


class TestDataLoader:
    """Test cases for DataLoader class."""
    
    def test_init_default(self):
        """Test default initialization."""
        loader = DataLoader()
        assert loader.engine == "pandas"
    
    def test_init_pandas(self):
        """Test initialization with pandas engine."""
        loader = DataLoader(engine="pandas")
        assert loader.engine == "pandas"
    
    def test_init_invalid_engine(self):
        """Test initialization with invalid engine."""
        with pytest.raises(ValueError, match="Engine must be"):
            DataLoader(engine="invalid")
    
    def test_load_csv(self, sample_csv_file, sample_df):
        """Test loading CSV file."""
        loader = DataLoader()
        df = loader.load_csv(sample_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == sample_df.shape
        assert list(df.columns) == list(sample_df.columns)
    
    def test_load_csv_not_found(self):
        """Test loading non-existent CSV file."""
        loader = DataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_csv("nonexistent.csv")
    
    def test_load_json(self, sample_json_file, sample_df):
        """Test loading JSON file."""
        loader = DataLoader()
        df = loader.load_json(sample_json_file)
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == sample_df.shape
    
    def test_load_auto_detect_csv(self, sample_csv_file):
        """Test auto-detection of CSV format."""
        loader = DataLoader()
        df = loader.load(sample_csv_file)
        
        assert isinstance(df, pd.DataFrame)
    
    def test_load_auto_detect_json(self, sample_json_file):
        """Test auto-detection of JSON format."""
        loader = DataLoader()
        df = loader.load(sample_json_file)
        
        assert isinstance(df, pd.DataFrame)
    
    def test_load_unsupported_format(self, temp_dir):
        """Test loading unsupported file format."""
        filepath = temp_dir / "data.txt"
        filepath.write_text("test")
        
        loader = DataLoader()
        with pytest.raises(ValueError, match="Unsupported file format"):
            loader.load(filepath)
    
    def test_load_with_kwargs(self, sample_csv_file):
        """Test loading with additional kwargs."""
        loader = DataLoader()
        df = loader.load_csv(sample_csv_file, usecols=['id', 'name'])
        
        assert df.shape[1] == 2
        assert 'id' in df.columns
        assert 'name' in df.columns
