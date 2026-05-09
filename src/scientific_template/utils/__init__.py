"""
Utils Module
============

General utility functions and helpers.
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from functools import wraps
import time
from datetime import datetime


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        format_string: Custom format string for log messages
        
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Get or create logger
    logger = logging.getLogger('scientific_template')
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def set_style(style: str = "seaborn-v0_8", context: str = "notebook"):
    """
    Set matplotlib/seaborn plotting style.
    
    Args:
        style: Style name (e.g., "darkgrid", "whitegrid", "dark", "ticks")
        context: Context name (e.g., "paper", "notebook", "talk", "poster")
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    sns.set_style(style)
    sns.set_context(context)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 12


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from a YAML or JSON file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif config_path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")


def save_config(config: Dict[str, Any], config_path: Union[str, Path]):
    """
    Save configuration to a YAML or JSON file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration file
    """
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        if config_path.suffix in ['.yaml', '.yml']:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        elif config_path.suffix == '.json':
            json.dump(config, f, indent=2)
        else:
            # Default to YAML
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def timer(func):
    """
    Decorator to measure function execution time.
    
    Usage:
        @timer
        def my_function():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Get function name
        func_name = func.__name__
        
        # Log or print the elapsed time
        if elapsed_time < 1:
            print(f"{func_name} completed in {elapsed_time * 1000:.2f} ms")
        else:
            print(f"{func_name} completed in {elapsed_time:.2f} s")
        
        return result
    return wrapper


def get_timestamp(format_string: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current timestamp as a formatted string.
    
    Args:
        format_string: strftime format string
        
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format_string)


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path object for the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Key prefix for nested items
        sep: Separator between nested keys
        
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (values override dict1)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result