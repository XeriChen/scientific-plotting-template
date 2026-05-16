"""
测试工具模块
"""

import pytest
import os
import tempfile
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
import logging


class TestLogging:
    """日志设置测试"""
    
    def test_setup_logging(self, tmp_path):
        """测试日志设置"""
        log_file = tmp_path / "test.log"
        logger = setup_logging(level="INFO", log_file=str(log_file))
        
        assert logger is not None
        assert logger.level == logging.INFO
        
        logger.info("Test log message")
        assert log_file.exists()
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert "Test log message" in content


class TestConfiguration:
    """配置管理测试"""
    
    def test_load_config_yaml(self, tmp_path):
        """测试加载YAML配置"""
        config_content = """
project:
  name: "Test Project"
  version: "0.1.0"
plotting:
  style: "seaborn-v0_8"
  dpi: 300
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        
        config = load_config(str(config_file))
        assert config["project"]["name"] == "Test Project"
        assert config["plotting"]["dpi"] == 300
    
    def test_save_config(self, tmp_path):
        """测试保存配置"""
        config = {
            "key1": "value1",
            "nested": {
                "key2": 42
            }
        }
        output_file = tmp_path / "output.yaml"
        
        save_config(config, str(output_file))
        assert output_file.exists()
        
        loaded = load_config(str(output_file))
        assert loaded["key1"] == "value1"
        assert loaded["nested"]["key2"] == 42


class TestTimer:
    """计时器装饰器测试"""
    
    def test_timer_decorator(self, capfd):
        """测试计时器装饰器"""
        @timer
        def fast_function():
            pass
        
        fast_function()
        
        captured = capfd.readouterr()
        assert "completed in" in captured.out


class TestFileUtils:
    """文件工具函数测试"""
    
    def test_ensure_dir(self, tmp_path):
        """测试确保目录存在"""
        new_dir = tmp_path / "new" / "nested" / "directory"
        result = ensure_dir(new_dir)
        
        assert result.exists()
        assert result.is_dir()
        assert str(result) == str(new_dir)
    
    def test_get_timestamp(self):
        """测试获取时间戳"""
        timestamp = get_timestamp()
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0
        
        custom_timestamp = get_timestamp("%Y-%m-%d")
        assert isinstance(custom_timestamp, str)
        assert len(custom_timestamp) == 10


class TestDictUtils:
    """字典工具函数测试"""
    
    def test_flatten_dict(self):
        """测试扁平化字典"""
        nested = {
            "a": 1,
            "b": {
                "c": 2,
                "d": {
                    "e": 3
                }
            }
        }
        
        flat = flatten_dict(nested)
        assert flat["a"] == 1
        assert flat["b.c"] == 2
        assert flat["b.d.e"] == 3
    
    def test_deep_merge(self):
        """测试深度合并字典"""
        dict1 = {
            "a": 1,
            "b": {"c": 2},
            "d": 3
        }
        dict2 = {
            "b": {"c": 20, "e": 4},
            "d": 30,
            "f": 5
        }
        
        merged = deep_merge(dict1, dict2)
        assert merged["a"] == 1
        assert merged["b"]["c"] == 20
        assert merged["b"]["e"] == 4
        assert merged["d"] == 30
        assert merged["f"] == 5


class TestStyle:
    """样式设置测试"""
    
    def test_set_style(self):
        """测试设置样式"""
        # 这个测试主要验证函数不会抛出异常
        try:
            set_style(style="seaborn-v0_8", context="notebook")
        except Exception as e:
            pytest.fail(f"set_style raised an exception: {e}")
