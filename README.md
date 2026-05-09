# Scientific Plotting Template

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-red.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: mypy](https://img.shields.io/badge/type%20checked-mypy-orange.svg)](http://mypy-lang.org/)

**A modern Python data analysis and visualization workspace**

</div>

---

## 📖 目录

- [简介](#-简介)
- [特性](#-特性)
- [安装](#-安装)
- [快速开始](#-快速开始)
- [模块概览](#-模块概览)
- [使用示例](#-使用示例)
- [命令行工具](#-命令行工具)
- [项目结构](#-项目结构)
- [开发指南](#-开发指南)
- [许可证](#-许可证)

---

## 🎯 简介

Scientific Plotting Template 是一个功能完整的 Python 数据分析与可视化工作区模板，专为科学计算和数据科学工作流设计。它集成了数据处理、统计分析、机器学习和可视化的一站式解决方案。

### 核心价值

- 🔧 **开箱即用** - 预配置的最佳实践和工具链
- 📊 **全功能支持** - 从数据加载到模型部署的完整流程
- 🚀 **高性能** - 支持 pandas 和 polars 双后端
- 📦 **模块化设计** - 清晰的分层架构，易于扩展
- 🎨 **出版级可视化** - 支持多种绘图库和样式

---

## ✨ 特性

### 数据处理
- ✅ 多格式数据加载（CSV, Excel, JSON, Parquet, Feather）
- ✅ 数据清洗与验证（缺失值、异常值、数据类型）
- ✅ 数据转换与重塑（标准化、编码、分箱）
- ✅ 支持 pandas 和 polars 双引擎

### 统计分析
- ✅ 描述性统计
- ✅ 假设检验（t 检验、ANOVA、卡方检验）
- ✅ 相关性分析（Pearson、Spearman）
- ✅ 正态性检验
- ✅ 置信区间计算

### 机器学习
- ✅ 模型训练管道
- ✅ 交叉验证
- ✅ 网格搜索超参数调优
- ✅ 分类与回归指标评估
- ✅ 支持 scikit-learn、XGBoost、LightGBM

### 可视化
- ✅ 7+ 种图表类型（线图、散点图、柱状图、直方图、箱线图、热力图等）
- ✅ 支持 matplotlib、seaborn、plotly、bokeh
- ✅ 出版级图像质量（300 DPI）
- ✅ 可定制样式和主题

### 实用工具
- ✅ 日志记录配置
- ✅ YAML/JSON 配置管理
- ✅ 性能计时器
- ✅ 命令行接口（CLI）

---

## 📥 安装

### 基础安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/scientific-plotting-template.git
cd scientific-plotting-template

# 使用 pip 安装
pip install -e .

# 或使用 uv（推荐）
uv pip install -e .
```

### 完整安装（包含所有依赖）

```bash
pip install -e ".[dev]"
```

### 可选依赖

```bash
# 开发工具
pip install -e ".[dev]"

# 测试工具
pip install -e ".[test]"

# 文档工具
pip install -e ".[docs]"
```

---

## 🚀 快速开始

### 5 分钟上手

```python
from scientific_template import DataLoader, DataProcessor, Plotter, StatisticalAnalyzer

# 1. 加载数据
loader = DataLoader()
df = loader.load_csv("data/my_data.csv")

# 2. 数据清洗
processor = DataProcessor()
df_clean = processor.remove_duplicates(df)
df_clean = processor.handle_missing(df_clean, strategy="fill_mean")

# 3. 统计分析
analyzer = StatisticalAnalyzer()
stats = analyzer.descriptive_stats(df_clean)
print(stats)

# 4. 可视化
plotter = Plotter()
fig = plotter.create_line_plot(df_clean, x="date", y="value", title="Time Series")
plotter.save_figure(fig, "output/plot.png")
```

### Jupyter Notebook 示例

```python
# 在 Jupyter 中快速开始
from scientific_template import *

# 设置样式
set_style("seaborn-v0_8", "notebook")

# 一键分析
df = DataLoader().load("data/dataset.csv")
StatisticalAnalyzer.descriptive_stats(df)
Plotter().create_correlation_matrix(df, save_path="output/corr_heatmap.png")
```

---

## 📦 模块概览

### 数据模块 (`scientific_template.data`)

| 类 | 功能 |
|-----|------|
| `DataLoader` | 多格式数据加载 |
| `DataProcessor` | 数据处理（去重、缺失值、排序等） |
| `DataCleaner` | 数据清洗（标准化列名、去除特殊字符等） |
| `DataTransformer` | 数据转换（标准化、编码、分箱等） |

### 统计模块 (`scientific_template.stats`)

| 类/函数 | 功能 |
|---------|------|
| `StatisticalAnalyzer` | 统计分析主类 |
| `perform_ttest()` | t 检验便捷函数 |
| `perform_anova()` | 方差分析便捷函数 |

### 机器学习模块 (`scientific_template.ml`)

| 类 | 功能 |
|-----|------|
| `ModelPipeline` | 模型训练与评估管道 |
| `CrossValidator` | 交叉验证与网格搜索 |

### 可视化模块 (`scientific_template.plotting`)

| 类/函数 | 功能 |
|---------|------|
| `Plotter` | 主绘图类 |
| `create_figure()` | 创建图形对象 |
| `save_figure()` | 保存图形 |

### 工具模块 (`scientific_template.utils`)

| 函数 | 功能 |
|------|------|
| `setup_logging()` | 配置日志 |
| `set_style()` | 设置绘图样式 |
| `load_config()` / `save_config()` | 配置管理 |
| `timer` | 性能计时装饰器 |

---

## 💻 使用示例

### 完整数据分析流程

```python
from scientific_template import (
    DataLoader, DataProcessor, DataCleaner, DataTransformer,
    StatisticalAnalyzer, Plotter, ModelPipeline, CrossValidator
)
from sklearn.ensemble import RandomForestClassifier

# ===== 1. 数据加载 =====
loader = DataLoader(engine="pandas")
df = loader.load_csv("data/sales_data.csv")

# ===== 2. 数据清洗 =====
cleaner = DataCleaner()
df = cleaner.standardize_column_names(df, case="snake")
df = cleaner.remove_whitespace(df)
df = cleaner.fix_data_types(df)

# ===== 3. 数据处理 =====
processor = DataProcessor()
df = processor.remove_duplicates(df)
df = processor.handle_missing(df, strategy="fill_median")

# ===== 4. 数据转换 =====
transformer = DataTransformer()
df = transformer.normalize(df, columns=["price", "quantity"], method="zscore")
df = transformer.encode_categorical(df, columns=["category"], method="onehot")

# ===== 5. 探索性分析 =====
plotter = Plotter()

# 创建多个图表
fig1 = plotter.create_histogram(df, column="price", title="Price Distribution")
fig2 = plotter.create_box_plot(df, x="category", y="price", title="Price by Category")
fig3 = plotter.create_correlation_matrix(df, title="Feature Correlations")

# 保存图表
plotter.save_figure(fig1, "output/price_hist.png")
plotter.save_figure(fig2, "output/price_box.png")
plotter.save_figure(fig3, "output/correlation.png")

# ===== 6. 统计分析 =====
analyzer = StatisticalAnalyzer()

# 描述性统计
desc_stats = analyzer.descriptive_stats(df)
print(desc_stats)

# 相关性分析
corr_result = analyzer.pearson_correlation(df["price"], df["quantity"])
print(f"Pearson correlation: {corr_result}")

# ===== 7. 机器学习 =====
# 准备数据
X = df.drop("target_column", axis=1)
y = df["target_column"]

# 训练模型
pipeline = ModelPipeline(model=RandomForestClassifier(n_estimators=100))
results = pipeline.fit(X, y, test_size=0.2)

print(f"Accuracy: {results['metrics']['accuracy']:.4f}")
print(f"F1 Score: {results['metrics']['f1']:.4f}")

# 交叉验证
cv = CrossValidator(cv=5)
cv_results = cv.validate(RandomForestClassifier(), X, y, scoring="accuracy")
print(f"CV Accuracy: {cv_results['mean_score']:.4f} (+/- {cv_results['std_score']:.4f})")
```

### 使用 Polars 后端处理大数据

```python
import polars as pl
from scientific_template import DataLoader, DataProcessor

# 使用 polars 引擎处理大型数据集
loader = DataLoader(engine="polars")
df = loader.load_csv("data/large_dataset.csv")

processor = DataProcessor(engine="polars")
df = processor.remove_duplicates(df)
df = processor.handle_missing(df, strategy="fill_mean")

# Polars 的高性能操作
result = (
    df
    .filter(pl.col("value") > 100)
    .group_by("category")
    .agg([
        pl.col("value").mean().alias("avg_value"),
        pl.col("value").sum().alias("total_value"),
    ])
    .sort("avg_value", descending=True)
)
```

---

## 🛠️ 命令行工具

安装后可使用 `spt` 命令：

```bash
# 查看帮助
spt --help

# 初始化新项目
spt init

# 查看数据文件信息
spt info --input data/myfile.csv

# 配置绘图样式
spt config-style --style seaborn-v0_8 --context notebook

# 读取配置文件
spt config-get --config-file config.yaml

# 保存配置
spt config-save '{"project": {"name": "My Project"}}' --output config.yaml
```

---

## 📁 项目结构

```
scientific-plotting-template/
├── src/scientific_template/    # 主包
│   ├── __init__.py
│   ├── cli.py                  # 命令行接口
│   ├── data/                   # 数据处理模块
│   │   ├── __init__.py
│   │   ├── loader.py           # 数据加载
│   │   ├── processor.py        # 数据处理
│   │   ├── clean.py            # 数据清洗
│   │   └── transform.py        # 数据转换
│   ├── plotting/               # 可视化模块
│   │   └── __init__.py         # 绘图工具
│   ├── stats/                  # 统计模块
│   │   └── __init__.py         # 统计分析
│   ├── ml/                     # 机器学习模块
│   │   └── __init__.py         # ML 工具
│   └── utils/                  # 工具模块
│       └── __init__.py         # 通用工具
├── tests/                      # 测试套件
├── docs/                       # 文档
├── examples/                   # 示例脚本
├── notebooks/                  # Jupyter notebooks
├── data/                       # 示例数据
├── output/                     # 输出目录
├── pyproject.toml              # 项目配置
├── README.md                   # 本文件
└── USAGE.md                    # 详细使用文档
```

---

## 👨‍💻 开发指南

### 环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -e ".[dev,test]"

# 安装 pre-commit hooks
pre-commit install
```

### 代码质量

```bash
# 运行 linter
ruff check .

# 格式化代码
ruff format .

# 类型检查
mypy src/

# 运行测试
pytest --cov=scientific_template
```

### 添加新功能

1. 在相应模块下创建新文件
2. 编写单元测试
3. 更新 `__init__.py` 导出
4. 运行测试确保通过
5. 更新文档

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献

欢迎贡献！请查看我们的贡献指南：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 📬 联系方式

- **作者**: Your Name
- **邮箱**: your.email@example.com
- **项目链接**: [GitHub](https://github.com/yourusername/scientific-plotting-template)

---

<div align="center">

**Made with ❤️ for the scientific Python community**

[⬆ 返回顶部](#scientific-plotting-template)

</div>
