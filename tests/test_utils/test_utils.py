"""
Tests for the utils module.
"""
import pytest
import json
import yaml
import logging
from pathlib import Path
from scientific_template.utils import (
    setup_logging,
    set_style,
    load_config,
    save_config,
    timer,
    get_timestamp,
    ensure_dir,
    flatten_dict,
    deep_merge
)


class TestLogging:
    """Test logging utilities."""
    
    def test_setup_logging(self):
        """Test setting up logging."""
        logger = setup_logging(level=logging.INFO)
        
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1
    
    def test_setup_logging_with_file(self, temp_dir):
        """Test setting up logging with file handler."""
        log_file = temp_dir / "test.log"
        logger = setup_logging(level=logging.DEBUG, log_file=log_file)
        
        assert len(logger.handlers) == 2  # Console + File
        assert log_file.exists()


class TestConfig:
    """Test configuration utilities."""
    
    def test_load_config_yaml(self, temp_dir):
        """Test loading YAML config."""
        config_file = temp_dir / "config.yaml"
        config = {"project": {"name": "Test", "version": "1.0"}}
        
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
        
        loaded = load_config(config_file)
        
        assert loaded == config
        assert loaded['project']['name'] == "Test"
    
    def test_load_config_json(self, temp_dir):
        """Test loading JSON config."""
        config_file = temp_dir / "config.json"
        config = {"project": {"name": "Test", "version": "1.0"}}
        
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        loaded = load_config(config_file)
        
        assert loaded == config
    
    def test_load_config_not_found(self):
        """Test loading non-existent config."""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yaml")
    
    def test_save_config_yaml(self, temp_dir):
        """Test saving YAML config."""
        config_file = temp_dir / "config.yaml"
        config = {"project": {"name": "Test"}}
        
        save_config(config, config_file)
        
        assert config_file.exists()
        
        with open(config_file, 'r') as f:
            loaded = yaml.safe_load(f)
        
        assert loaded == config
    
    def test_save_config_json(self, temp_dir):
        """Test saving JSON config."""
        config_file = temp_dir / "config.json"
        config = {"project": {"name": "Test"}}
        
        save_config(config, config_file)
        
        assert config_file.exists()
        
        with open(config_file, 'r') as f:
            loaded = json.load(f)
        
        assert loaded == config


class TestHelpers:
    """Test helper functions."""
    
    def test_get_timestamp(self):
        """Test getting timestamp."""
        ts = get_timestamp()
        
        assert isinstance(ts, str)
        assert len(ts) > 0
    
    def test_get_timestamp_custom_format(self):
        """Test getting timestamp with custom format."""
        ts = get_timestamp("%Y-%m-%d")
        
        assert len(ts) == 10  # YYYY-MM-DD
    
    def test_ensure_dir(self, temp_dir):
        """Test ensuring directory exists."""
        new_dir = temp_dir / "subdir" / "nested"
        
        result = ensure_dir(new_dir)
        
        assert result.exists()
        assert result.is_dir()
    
    def test_flatten_dict(self):
        """Test flattening nested dictionary."""
        nested = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'e': 3
                }
            }
        }
        
        flat = flatten_dict(nested)
        
        assert flat == {'a': 1, 'b.c': 2, 'b.d.e': 3}
    
    def test_deep_merge(self):
        """Test deep merging dictionaries."""
        dict1 = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            }
        }
        
        dict2 = {
            'b': {
                'c': 20,
                'e': 4
            },
            'f': 5
        }
        
        merged = deep_merge(dict1, dict2)
        
        assert merged['a'] == 1
        assert merged['b']['c'] == 20  # Overridden
        assert merged['b']['d'] == 3   # Preserved
        assert merged['b']['e'] == 4   # Added
        assert merged['f'] == 5        # Added


class TestTimer:
    """Test timer decorator."""
    
    def test_timer_decorator(self, capsys):
        """Test timer decorator outputs execution time."""
        
        @timer
        def quick_function():
            return 42
        
        result = quick_function()
        
        assert result == 42
        captured = capsys.readouterr()
        assert "quick_function" in captured.out
        assert ("ms" in captured.out or "s" in captured.out)
