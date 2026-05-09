# Scientific Template 使用文档

## 📖 目录

- [简介](#简介)
- [安装](#安装)
- [快速开始](#快速开始)
- [模块详解](#模块详解)
  - [数据模块 (data)](#数据模块-data)
  - [可视化模块 (plotting)](#可视化模块-plotting)
  - [统计模块 (stats)](#统计模块-stats)
  - [机器学习模块 (ml)](#机器学习模块-ml)
  - [工具模块 (utils)](#工具模块-utils)
- [命令行工具](#命令行工具)
- [配置管理](#配置管理)
- [最佳实践](#最佳实践)
- [示例代码](#示例代码)

---

## 简介

**Scientific Template** 是一个现代化的 Python 数据分析与可视化工作区，提供了一套完整的工具用于：

- 📊 **数据处理**：支持多种格式的数据加载、清洗和转换
- 📈 **可视化**：创建出版级的科学图表
- 📉 **统计分析**：执行常用的统计检验和分析
- 🤖 **机器学习**： streamlined 模型训练和评估流程
- 🛠️ **实用工具**：日志、配置、计时器等辅助功能

### 核心特性

- **双后端支持**：兼容 pandas 和 polars，可根据需求选择
- **模块化设计**：清晰的模块划分，易于扩展和维护
- **类型安全**：完整的类型注解，支持静态类型检查
- **CLI 工具**：便捷的命令行接口
- **最佳实践**：遵循科学计算和可重复研究的标准

---

## 安装

### 基础安装

```bash
pip install -e .
```

### 开发环境安装

```bash
pip install -e ".[dev]"
```

### 可选依赖

```bash
# 仅安装测试依赖
pip install -e ".[test]"

# 仅安装文档依赖
pip install -e ".[docs]"
```

### 依赖要求

- Python >= 3.9
- 主要依赖：pandas, numpy, matplotlib, seaborn, scipy, scikit-learn

---

## 快速开始

```python
from scientific_template import (
    DataLoader, DataProcessor, Plotter, 
    StatisticalAnalyzer, ModelPipeline,
    setup_logging, load_config
)

# 1. 设置日志
logger = setup_logging(level="INFO")

# 2. 加载数据
loader = DataLoader(engine="pandas")
df = loader.load_csv("data/my_data.csv")

# 3. 数据处理
processor = DataProcessor()
df_clean = processor.remove_duplicates(df)
df_clean = processor.handle_missing(df_clean, strategy="fill_mean")

# 4. 描述性统计
analyzer = StatisticalAnalyzer()
stats = analyzer.descriptive_stats(df_clean)
print(stats)

# 5. 可视化
plotter = Plotter(style="seaborn-v0_8")
fig = plotter.create_line_plot(
    data=df_clean,
    x="time",
    y="value",
    title="Time Series Analysis"
)

# 6. 保存图表
plotter.save_figure(fig, "output/analysis.png")
```

---

## 模块详解

### 数据模块 (data)

数据模块提供完整的数据处理管道，包括加载、清洗、处理和转换。

#### DataLoader - 数据加载器

支持多种文件格式的自动检测和加载。

```python
from scientific_template.data import DataLoader

# 初始化（支持 pandas 或 polars 后端）
loader = DataLoader(engine="pandas")  # 或 engine="polars"

# 自动检测格式加载
df = loader.load("data/file.csv")
df = loader.load("data/file.xlsx")
df = loader.load("data/file.json")
df = loader.load("data/file.parquet")

# 指定格式加载
df = loader.load_csv("data/file.csv", sep=",")
df = loader.load_excel("data/file.xlsx", sheet_name="Sheet1")
df = loader.load_json("data/file.json")
df = loader.load_parquet("data/file.parquet")
```

**支持的文件格式**：
- CSV / TSV
- Excel (.xlsx, .xls)
- JSON
- Parquet
- Feather

#### DataProcessor - 数据处理器

提供常用的数据处理操作。

```python
from scientific_template.data import DataProcessor

processor = DataProcessor(engine="pandas")

# 删除重复值
df = processor.remove_duplicates(df, subset=["col1", "col2"], keep="first")

# 处理缺失值
df = processor.handle_missing(df, strategy="drop")  # 删除
df = processor.handle_missing(df, strategy="fill_mean")  # 均值填充
df = processor.handle_missing(df, strategy="fill_median")  # 中位数填充
df = processor.handle_missing(df, strategy="fill_mode")  # 众数填充
df = processor.handle_missing(df, strategy="fill_value", fill_value=0)  # 指定值填充

# 重命名列
df = processor.rename_columns(df, {"old_name": "new_name"})

# 选择列
df = processor.select_columns(df, ["col1", "col2"])

# 过滤行
df = processor.filter_rows(df, lambda x: x["value"] > 100)

# 排序
df = processor.sort_values(df, by="value", ascending=False)

# 添加新列
df = processor.add_column(df, "new_col", values=0)  # 标量值
df = processor.add_column(df, "computed", lambda row: row["a"] + row["b"])  # 函数

# 获取数据信息
info = processor.get_info(df)
print(info)  # {'shape': (100, 5), 'columns': [...], 'dtypes': {...}, ...}
```

#### DataCleaner - 数据清洗器

处理数据质量问题和标准化。

```python
from scientific_template.data import DataCleaner

cleaner = DataCleaner(engine="pandas")

# 标准化列名
df = cleaner.standardize_column_names(df, case="snake")  # snake_case
# "Column Name" -> "column_name"

# 去除空白字符
df = cleaner.remove_whitespace(df, columns=["name", "address"])

# 修复数据类型
df = cleaner.fix_data_types(df, column_types={"age": "int", "price": "float"})

# 移除特殊字符
df = cleaner.remove_special_characters(df, columns=["text"], pattern=r'[^a-zA-Z0-9\s]')

# 验证邮箱
df = cleaner.validate_email(df, column="email", remove_invalid=True)

# 检测异常值（IQR 方法）
outliers = cleaner.detect_outliers_iqr(df, columns=["value"], multiplier=1.5)

# 清理货币列
df = cleaner.clean_currency(df, columns=["price"])  # "$1,234.56" -> 1234.56
```

#### DataTransformer - 数据转换器

数据变换和重塑操作。

```python
from scientific_template.data import DataTransformer

transformer = DataTransformer(engine="pandas")

# 归一化
df = transformer.normalize(df, method="minmax")  # [0, 1] 范围
df = transformer.normalize(df, method="zscore")  # Z-score 标准化
df = transformer.normalize(df, method="robust")  # 稳健标准化

# 编码分类变量
df = transformer.encode_categorical(df, columns=["category"], method="onehot")
df = transformer.encode_categorical(df, method="label")  # 标签编码
df = transformer.encode_categorical(df, method="frequency")  # 频率编码

# 透视表
pivot_df = transformer.pivot(df, index="date", columns="category", values="value", aggfunc="mean")

# 熔融（宽表转长表）
long_df = transformer.melt(df, id_vars=["id"], value_vars=["col1", "col2"])

# 分箱
df = transformer.binning(df, column="age", bins=5, labels=["young", "mid", "old"])

# 对数变换
df = transformer.log_transform(df, columns=["income"], base=np.e)

# 滚动窗口
rolling_mean = transformer.rolling_window(df, column="value", window=7, operation="mean")
```

---

### 可视化模块 (plotting)

提供创建出版级图表的工具。

#### Plotter - 绘图器

```python
from scientific_template.plotting import Plotter

# 初始化
plotter = Plotter(style="seaborn-v0_8", context="notebook")

# 线图
fig = plotter.create_line_plot(
    data=df,
    x="time",
    y="value",
    hue="category",  # 可选：按类别分组
    title="Time Series",
    xlabel="Time",
    ylabel="Value",
    figsize=(12, 6),
    save_path="output/line_plot.png"  # 可选：保存路径
)

# 散点图
fig = plotter.create_scatter_plot(
    data=df,
    x="x_var",
    y="y_var",
    hue="group",
    size="size_var",  # 可选：点大小
    title="Scatter Plot",
    figsize=(10, 8)
)

# 柱状图
fig = plotter.create_bar_plot(
    data=df,
    x="category",
    y="value",
    hue="subcategory",  # 可选：分组
    title="Bar Chart"
)

# 直方图
fig = plotter.create_histogram(
    data=df,
    column="value",
    hue="group",  # 可选：分组
    bins=30,
    title="Distribution"
)

# 箱线图
fig = plotter.create_box_plot(
    data=df,
    x="category",
    y="value",
    hue="group",
    title="Box Plot"
)

# 热力图
fig = plotter.create_heatmap(
    data=corr_matrix,
    annot=True,
    cmap="coolwarm",
    title="Correlation Heatmap"
)

# 相关矩阵
fig = plotter.create_correlation_matrix(
    data=df,
    method="pearson",  # 或 "spearman", "kendall"
    annot=True,
    title="Correlation Matrix",
    save_path="output/correlation.png"
)
```

#### 辅助函数

```python
from scientific_template.plotting import create_figure, save_figure

# 创建自定义图形
fig, ax = create_figure(figsize=(10, 6), dpi=300)

# 保存图形
save_figure(fig, "output/my_plot.pdf", dpi=300, bbox_inches='tight')
```

---

### 统计模块 (stats)

提供常用的统计分析功能。

#### StatisticalAnalyzer - 统计分析器

```python
from scientific_template.stats import StatisticalAnalyzer

analyzer = StatisticalAnalyzer()

# 描述性统计
stats = analyzer.descriptive_stats(df)
print(stats)

# 独立样本 t 检验
result = analyzer.ttest_independent(group1, group2, equal_var=True)
print(f"t={result['t_statistic']:.3f}, p={result['p_value']:.4f}")

# 配对样本 t 检验
result = analyzer.ttest_paired(before, after)

# 单因素方差分析 (ANOVA)
result = analyzer.anova_one_way(group1, group2, group3)
print(f"F={result['f_statistic']:.3f}, p={result['p_value']:.4f}")

# 卡方检验
result = analyzer.chi_square_test(observed_table)
print(f"χ²={result['chi_square']:.3f}, p={result['p_value']:.4f}")

# 相关矩阵
corr = analyzer.correlation(df, method="pearson")

# Pearson 相关系数
result = analyzer.pearson_correlation(x, y)
print(f"r={result['correlation']:.3f}, p={result['p_value']:.4f}")

# Spearman 秩相关
result = analyzer.spearman_correlation(x, y)

# 正态性检验
result = analyzer.normality_test(data, method="shapiro")
print(f"stat={result['statistic']:.3f}, p={result['p_value']:.4f}")

# 置信区间
ci = analyzer.confidence_interval(data, confidence=0.95)
print(f"95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")
```

#### 便捷函数

```python
from scientific_template.stats import perform_ttest, perform_anova

# t 检验
result = perform_ttest(group1, group2, paired=False, equal_var=True)

# ANOVA
result = perform_anova(group1, group2, group3)
```

---

### 机器学习模块 (ml)

提供简化的机器学习工作流。

#### ModelPipeline - 模型管道

```python
from scientific_template.ml import ModelPipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# 初始化（自动包含特征缩放）
pipeline = ModelPipeline(model=LinearRegression(), scaler=True)

# 训练和评估
results = pipeline.fit(X, y, test_size=0.2, random_state=42)

# 查看结果
print("Metrics:", results["metrics"])
# 回归：{'mse': ..., 'rmse': ..., 'r2': ...}
# 分类：{'accuracy': ..., 'precision': ..., 'recall': ..., 'f1': ...}

# 预测
predictions = pipeline.predict(X_new)

# 评估
metrics = pipeline.evaluate(X_test, y_test)
```

#### CrossValidator - 交叉验证器

```python
from scientific_template.ml import CrossValidator
from sklearn.svm import SVC

cv = CrossValidator(cv=5)  # 5 折交叉验证

# 交叉验证
results = cv.validate(
    model=SVC(),
    X=X,
    y=y,
    scoring="accuracy",  # 可选：指定评分指标
    shuffle=True,
    random_state=42
)

print(f"Mean Score: {results['mean_score']:.3f} ± {results['std_score']:.3f}")
print(f"Scores: {results['scores']}")
print(f"Range: [{results['min_score']:.3f}, {results['max_score']:.3f}]")

# 网格搜索
param_grid = {
    "C": [0.1, 1, 10],
    "kernel": ["linear", "rbf"]
}

grid_results = cv.grid_search(
    model=SVC(),
    X=X,
    y=y,
    param_grid=param_grid,
    scoring="accuracy"
)

print("Best Parameters:", grid_results["best_params"])
print("Best Score:", grid_results["best_score"])
```

---

### 工具模块 (utils)

通用工具函数和辅助功能。

```python
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

# 设置日志
logger = setup_logging(
    level="INFO",
    log_file="logs/app.log",
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger.info("Application started")

# 设置绘图风格
set_style(style="seaborn-v0_8", context="paper")

# 加载配置
config = load_config("config.yaml")
config = load_config("config.json")

# 保存配置
save_config({"key": "value"}, "output/config.yaml")

# 计时器装饰器
@timer
def slow_function():
    import time
    time.sleep(2)

slow_function()  # 输出：slow_function completed in 2.00 s

# 获取时间戳
timestamp = get_timestamp()  # "20240101_120000"
timestamp = get_timestamp("%Y-%m-%d %H:%M:%S")  # "2024-01-01 12:00:00"

# 确保目录存在
data_dir = ensure_dir("data/output")

# 扁平化嵌套字典
nested = {"a": {"b": 1, "c": 2}}
flat = flatten_dict(nested)  # {"a.b": 1, "a.c": 2}

# 深度合并字典
dict1 = {"a": 1, "b": {"c": 2}}
dict2 = {"b": {"d": 3}, "e": 4}
merged = deep_merge(dict1, dict2)  # {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
```

---

## 命令行工具

安装后可使用 `spt` 命令：

```bash
# 查看帮助
spt --help

# 查看版本
spt --version

# 问候命令
spt hello --name "World"

# 查看数据文件信息
spt info -i data/file.csv
spt info -i data/file.xlsx --format excel

# 配置绘图风格
spt config-style --style seaborn-v0_8 --context paper

# 读取配置
spt config-get -c config.yaml
spt config-get -c config.yaml -k project.name

# 保存配置
spt config-save '{"key": "value"}' -o config.yaml

# 初始化新项目
spt init
```

### `spt init` 创建的目录结构

```
my_project/
├── data/           # 数据目录
│   ├── input/      # 输入数据
│   └── output/     # 输出数据
├── notebooks/      # Jupyter notebooks
├── examples/       # 示例代码
├── tests/          # 测试文件
├── docs/           # 文档
├── output/         # 分析输出
└── config.yaml     # 配置文件
```

---

## 配置管理

### 配置文件格式

支持 YAML 和 JSON 格式：

**config.yaml**:
```yaml
project:
  name: "My Analysis Project"
  version: "0.1.0"

data:
  input_dir: "data/input"
  output_dir: "data/output"

plotting:
  style: "seaborn-v0_8"
  context: "notebook"
  dpi: 300
  
logging:
  level: "INFO"
  file: "logs/app.log"

ml:
  test_size: 0.2
  random_state: 42
  cv_folds: 5
```

**config.json**:
```json
{
  "project": {
    "name": "My Analysis Project",
    "version": "0.1.0"
  },
  "plotting": {
    "style": "seaborn-v0_8",
    "dpi": 300
  }
}
```

### 在代码中使用配置

```python
from scientific_template.utils import load_config, set_style
import logging

# 加载配置
config = load_config("config.yaml")

# 应用配置
set_style(
    style=config["plotting"]["style"],
    context=config["plotting"]["context"]
)

# 设置日志
logging.basicConfig(level=getattr(logging, config["logging"]["level"]))
```

---

## 最佳实践

### 1. 项目结构

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── data_processing.py
│       └── analysis.py
├── data/
│   ├── raw/          # 原始数据（不修改）
│   ├── processed/    # 处理后的数据
│   └── external/     # 外部数据
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_modeling.ipynb
├── output/
│   ├── figures/      # 图表
│   ├── tables/       # 表格
│   └── models/       # 模型文件
├── tests/
├── config.yaml
├── pyproject.toml
└── README.md
```

### 2. 可重复性

```python
# 始终设置随机种子
import numpy as np
np.random.seed(42)

# 在模型训练中使用 random_state
from scientific_template.ml import ModelPipeline
pipeline = ModelPipeline(model=..., scaler=True)
results = pipeline.fit(X, y, random_state=42)

# 记录版本信息
from scientific_template import __version__
print(f"Using scientific-template v{__version__}")
```

### 3. 性能优化

```python
# 大数据集使用 polars
loader = DataLoader(engine="polars")
df = loader.load_csv("large_file.csv")

# 使用适当的策略处理缺失值
processor = DataProcessor()
df = processor.handle_missing(df, strategy="fill_mean")

# 批量处理大文件
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)
```

### 4. 错误处理

```python
from scientific_template.data import DataLoader

loader = DataLoader()
try:
    df = loader.load("data/file.csv")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid file format: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 示例代码

### 完整分析流程

```python
"""
完整数据分析示例
"""
from scientific_template import (
    DataLoader, DataProcessor, DataCleaner, DataTransformer,
    Plotter, StatisticalAnalyzer, ModelPipeline, CrossValidator,
    setup_logging, load_config
)
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# 1. 初始化
logger = setup_logging(level="INFO", log_file="logs/analysis.log")
config = load_config("config.yaml")
logger.info("Starting analysis...")

# 2. 加载数据
loader = DataLoader(engine="pandas")
df = loader.load_csv("data/sales_data.csv")
logger.info(f"Loaded {len(df)} records")

# 3. 数据清洗
cleaner = DataCleaner()
df = cleaner.standardize_column_names(df)
df = cleaner.remove_whitespace(df)
df = cleaner.fix_data_types(df)

# 4. 数据处理
processor = DataProcessor()
df = processor.remove_duplicates(df)
df = processor.handle_missing(df, strategy="fill_median")

# 5. 数据转换
transformer = DataTransformer()
df = transformer.normalize(df, method="zscore")
df = transformer.encode_categorical(df, method="onehot")

# 6. 探索性分析
analyzer = StatisticalAnalyzer()
desc_stats = analyzer.descriptive_stats(df)
print(desc_stats)

# 相关性分析
corr = analyzer.correlation(df.select_dtypes(include=[np.number]))
print(corr)

# 7. 可视化
plotter = Plotter(style="seaborn-v0_8", context="notebook")

# 时间序列图
fig = plotter.create_line_plot(
    df, x="date", y="sales",
    title="Sales Over Time",
    save_path="output/sales_trend.png"
)

# 分布直方图
fig = plotter.create_histogram(
    df, column="sales",
    title="Sales Distribution",
    save_path="output/sales_dist.png"
)

# 相关矩阵热图
fig = plotter.create_correlation_matrix(
    df.select_dtypes(include=[np.number]),
    save_path="output/correlation.png"
)

# 8. 建模
X = df.drop("target", axis=1)
y = df["target"]

pipeline = ModelPipeline(model=RandomForestRegressor(n_estimators=100))
results = pipeline.fit(X, y, test_size=0.2)

logger.info(f"Model R²: {results['metrics']['r2']:.3f}")
logger.info(f"Model RMSE: {results['metrics']['rmse']:.3f}")

# 9. 交叉验证
cv = CrossValidator(cv=5)
cv_results = cv.validate(
    model=RandomForestRegressor(n_estimators=100),
    X=X, y=y,
    scoring="r2"
)

logger.info(f"CV R²: {cv_results['mean_score']:.3f} ± {cv_results['std_score']:.3f}")

# 10. 完成
logger.info("Analysis complete!")
```

### Jupyter Notebook 示例

```python
# notebook.ipynb

from scientific_template import *
import pandas as pd

# 快速设置
setup_logging()
Plotter.set_style("seaborn-v0_8", "notebook")

# 一行代码加载数据
df = DataLoader().load_csv("data.csv")

# 快速查看统计
StatisticalAnalyzer.descriptive_stats(df)

# 快速绘图
plotter = Plotter()
plotter.create_scatter_plot(df, "x", "y", hue="category")
```

---

## API 参考

### 类和方法索引

#### Data Module
- `DataLoader`
  - `load_csv()`, `load_excel()`, `load_json()`, `load_parquet()`, `load_feather()`
  - `load()` - 自动检测格式
- `DataProcessor`
  - `remove_duplicates()`, `handle_missing()`, `rename_columns()`
  - `select_columns()`, `filter_rows()`, `sort_values()`
  - `add_column()`, `get_info()`
- `DataCleaner`
  - `standardize_column_names()`, `remove_whitespace()`
  - `fix_data_types()`, `remove_special_characters()`
  - `validate_email()`, `detect_outliers_iqr()`, `clean_currency()`
- `DataTransformer`
  - `normalize()`, `encode_categorical()`
  - `pivot()`, `melt()`, `binning()`
  - `log_transform()`, `rolling_window()`

#### Plotting Module
- `Plotter`
  - `create_line_plot()`, `create_scatter_plot()`, `create_bar_plot()`
  - `create_histogram()`, `create_box_plot()`
  - `create_heatmap()`, `create_correlation_matrix()`
- `create_figure()`, `save_figure()`

#### Stats Module
- `StatisticalAnalyzer`
  - `descriptive_stats()`, `ttest_independent()`, `ttest_paired()`
  - `anova_one_way()`, `chi_square_test()`, `correlation()`
  - `pearson_correlation()`, `spearman_correlation()`
  - `normality_test()`, `confidence_interval()`
- `perform_ttest()`, `perform_anova()`

#### ML Module
- `ModelPipeline`
  - `fit()`, `predict()`, `evaluate()`
- `CrossValidator`
  - `validate()`, `grid_search()`

#### Utils Module
- `setup_logging()`, `set_style()`
- `load_config()`, `save_config()`
- `timer`, `get_timestamp()`, `ensure_dir()`
- `flatten_dict()`, `deep_merge()`

---

## 故障排除

### 常见问题

**Q: polars 导入失败？**
A: polars 是可选依赖。如果未安装，会自动降级到 pandas。如需使用 polars：
```bash
pip install polars
```

**Q: 图表显示中文乱码？**
A: 设置合适的字体：
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

**Q: 内存不足？**
A: 尝试使用 polars 后端或分块处理：
```python
loader = DataLoader(engine="polars")  # 更高效的内存使用
# 或
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)
```

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 许可证

MIT License - 详见 LICENSE 文件

---

## 联系方式

- 作者：Your Name
- 邮箱：your.email@example.com
- 项目主页：https://github.com/yourusername/scientific-plotting-template
