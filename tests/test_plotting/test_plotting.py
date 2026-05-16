"""
测试可视化模块
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scientific_template.plotting import Plotter, create_figure, save_figure
from scientific_template.utils import ensure_dir
import os


class TestPlotter:
    """Plotter类测试"""
    
    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        np.random.seed(42)
        return pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y': np.sin(np.linspace(0, 10, 100)) + np.random.randn(100) * 0.1,
            'category': ['A'] * 50 + ['B'] * 50,
            'value': np.random.randn(100)
        })
    
    def test_plotter_initialization(self):
        """测试Plotter初始化"""
        plotter = Plotter(style="seaborn-v0_8", context="notebook")
        assert plotter is not None
    
    def test_create_line_plot(self, sample_data):
        """测试创建线图"""
        plotter = Plotter()
        fig = plotter.create_line_plot(
            data=sample_data,
            x='x',
            y='y',
            title='Test Line Plot'
        )
        assert fig is not None
        plt.close(fig)
    
    def test_create_scatter_plot(self, sample_data):
        """测试创建散点图"""
        plotter = Plotter()
        fig = plotter.create_scatter_plot(
            data=sample_data,
            x='x',
            y='y',
            hue='category'
        )
        assert fig is not None
        plt.close(fig)
    
    def test_create_bar_plot(self, sample_data):
        """测试创建柱状图"""
        plotter = Plotter()
        fig = plotter.create_bar_plot(
            data=sample_data,
            x='category',
            y='value'
        )
        assert fig is not None
        plt.close(fig)
    
    def test_create_histogram(self, sample_data):
        """测试创建直方图"""
        plotter = Plotter()
        fig = plotter.create_histogram(
            data=sample_data,
            column='value',
            bins=20
        )
        assert fig is not None
        plt.close(fig)
    
    def test_create_box_plot(self, sample_data):
        """测试创建箱线图"""
        plotter = Plotter()
        fig = plotter.create_box_plot(
            data=sample_data,
            x='category',
            y='value'
        )
        assert fig is not None
        plt.close(fig)
    
    def test_create_heatmap(self):
        """测试创建热力图"""
        plotter = Plotter()
        data = np.random.rand(10, 10)
        fig = plotter.create_heatmap(data, annot=True)
        assert fig is not None
        plt.close(fig)
    
    def test_create_correlation_matrix(self, sample_data):
        """测试创建相关矩阵"""
        plotter = Plotter()
        numeric_data = sample_data[['x', 'y', 'value']]
        fig = plotter.create_correlation_matrix(numeric_data)
        assert fig is not None
        plt.close(fig)
    
    def test_save_figure(self, sample_data, tmp_path):
        """测试保存图表"""
        plotter = Plotter()
        fig = plotter.create_histogram(data=sample_data, column='value')
        output_path = tmp_path / "test_plot.png"
        plotter.save_figure(fig, output_path)
        assert output_path.exists()
        plt.close(fig)


class TestPlottingUtils:
    """绘图工具函数测试"""
    
    def test_create_figure(self):
        """测试创建图形"""
        fig, ax = create_figure(figsize=(10, 6), dpi=100)
        assert fig is not None
        assert ax is not None
        plt.close(fig)
    
    def test_save_figure(self, tmp_path):
        """测试保存图形"""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        output_path = tmp_path / "utils_test.png"
        save_figure(fig, output_path)
        assert output_path.exists()
        plt.close(fig)
