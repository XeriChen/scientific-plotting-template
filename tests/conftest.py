"""
Test fixtures and configuration for pytest.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 75000, 80000, 90000],
        'department': ['Engineering', 'Marketing', 'Engineering', 'Sales', 'Marketing'],
        'rating': [4.5, 3.8, 4.9, 4.2, 3.5]
    })


@pytest.fixture
def df_with_missing():
    """Create a DataFrame with missing values."""
    return pd.DataFrame({
        'a': [1, 2, np.nan, 4, 5],
        'b': [5, np.nan, 7, 8, 9],
        'c': [np.nan, 2, 3, 4, 5],
        'd': [1, 2, 3, 4, 5]
    })


@pytest.fixture
def df_with_duplicates():
    """Create a DataFrame with duplicates."""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 4, 4],
        'value': [10, 20, 20, 30, 40, 40]
    })


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    dirpath = tempfile.mkdtemp()
    yield Path(dirpath)
    shutil.rmtree(dirpath)


@pytest.fixture
def sample_csv_file(temp_dir, sample_df):
    """Create a temporary CSV file."""
    filepath = temp_dir / "sample.csv"
    sample_df.to_csv(filepath, index=False)
    return filepath


@pytest.fixture
def sample_excel_file(temp_dir, sample_df):
    """Create a temporary Excel file."""
    filepath = temp_dir / "sample.xlsx"
    sample_df.to_excel(filepath, index=False)
    return filepath


@pytest.fixture
def sample_json_file(temp_dir, sample_df):
    """Create a temporary JSON file."""
    filepath = temp_dir / "sample.json"
    sample_df.to_json(filepath, orient='records', indent=2)
    return filepath


@pytest.fixture
def numeric_data():
    """Create sample numeric data for statistical tests."""
    np.random.seed(42)
    group1 = np.random.normal(100, 15, 50)
    group2 = np.random.normal(105, 15, 50)
    group3 = np.random.normal(110, 15, 50)
    return {
        'group1': group1,
        'group2': group2,
        'group3': group3
    }


@pytest.fixture
def classification_data():
    """Create sample classification data."""
    np.random.seed(42)
    n_samples = 100
    
    X = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.randn(n_samples)
    })
    
    y = (X['feature1'] + X['feature2'] > 0).astype(int)
    
    return X, y


@pytest.fixture
def regression_data():
    """Create sample regression data."""
    np.random.seed(42)
    n_samples = 100
    
    X = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples)
    })
    
    y = 2 * X['feature1'] + 3 * X['feature2'] + np.random.randn(n_samples) * 0.5
    
    return X, y
