# UV 包管理器配置指南

## 概述

本项目已配置为支持现代化的 `uv` 包管理器。`uv` 是一个用 Rust 编写的超快速 Python 包安装器和解析器，比 pip 快 10-100 倍。

## 安装 UV

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 使用 pip
```bash
pip install uv
```

## 项目配置

### 核心依赖 (pyproject.toml)

本项目的 `pyproject.toml` 已优化为最小核心依赖集，以适应资源受限的环境：

```toml
dependencies = [
    # 数据处理 (核心)
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    
    # 可视化 (核心)
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    
    # 统计分析 (核心)
    "scipy>=1.11.0",
    "statsmodels>=0.14.0",
    
    # 机器学习 (核心)
    "scikit-learn>=1.3.0",
    
    # 实用工具
    "tqdm>=4.65.0",
    "rich>=13.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "click>=8.0.0",
]
```

### 可选依赖

其他功能（如交互式分析、地理空间、高级可视化等）已移至可选依赖：

```toml
[project.optional-dependencies]
viz = [
    "plotly>=5.15.0",
    "bokeh>=3.2.0",
]
ml = [
    "xgboost>=1.7.0",
    "lightgbm>=4.0.0",
]
geo = [
    "geopandas>=0.13.0",
    "folium>=0.14.0",
]
# ... 更多可选依赖见 pyproject.toml
```

## 使用方法

### 创建虚拟环境并安装依赖

```bash
# 仅安装核心依赖（推荐用于资源受限环境）
uv sync

# 安装所有依赖（包括开发依赖）
uv sync --all-extras --dev

# 安装特定可选依赖
uv sync --extra viz --extra ml
```

### 运行命令

```bash
# 在虚拟环境中运行命令
uv run python your_script.py

# 运行 CLI 工具
uv run spt --help

# 运行测试
uv run pytest
```

### 添加新依赖

```bash
# 添加核心依赖
uv add package-name

# 添加可选依赖到特定组
uv add --optional viz package-name

# 添加开发依赖
uv add --dev package-name
```

### 锁定依赖

```bash
# 更新锁文件
uv lock

# 重新解析所有依赖
uv lock --upgrade
```

## 环境要求

- **Python**: >= 3.9
- **磁盘空间**: 
  - 最小安装（核心依赖）: ~500MB
  - 完整安装（所有依赖）: ~2GB+
- **内存**: 建议 2GB+

## 故障排除

### 磁盘空间不足

如果遇到"No space left on device"错误：

1. 清理 uv 缓存：
   ```bash
   uv cache clean
   ```

2. 使用无缓存模式：
   ```bash
   uv sync --no-cache
   ```

3. 仅安装核心依赖：
   ```bash
   uv sync  # 不添加 --all-extras
   ```

### 指定缓存目录

```bash
export UV_CACHE_DIR=/path/to/larger/disk
uv sync
```

## 与传统 pip 的对比

| 特性 | uv | pip |
|------|-----|-----|
| 安装速度 | 10-100x 更快 | 基准 |
| 依赖解析 | 极快（Rust） | 较慢（Python） |
| 磁盘空间 | 全局缓存共享 | 每个环境独立 |
| 锁文件 | 原生支持 (uv.lock) | 需要 pip-tools |
| Python 管理 | 内置 (uv python) | 需要 pyenv/conda |

## 最佳实践

1. **始终提交 `uv.lock`**：确保团队和环境间的依赖一致性
2. **使用可选依赖**：按需安装，减少初始下载和安装时间
3. **利用全局缓存**：uv 自动在不同项目间共享包缓存
4. **定期更新**：`uv lock --upgrade` 保持依赖最新

## 迁移自 pip

如果你之前使用 pip/virtualenv：

```bash
# 旧方式
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 新方式（uv）
uv sync --dev
```

两者创建的虚拟环境兼容，可以互换使用。
