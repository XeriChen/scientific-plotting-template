# Git Commit Message Convention
# Git 提交信息规范

## Format 格式

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Type 类型

| Type | Description | 说明 |
|------|-------------|------|
| feat | New feature | 新功能 |
| fix | Bug fix | 修复bug |
| docs | Documentation only | 仅文档修改 |
| style | Code style (formatting, semicolons, etc) | 代码格式修改 |
| refactor | Code refactoring | 重构 |
| perf | Performance improvements | 性能优化 |
| test | Adding or updating tests | 测试相关 |
| chore | Build process or auxiliary tool changes | 构建/工具变更 |
| ci | CI configuration changes | CI配置 |
| revert | Revert to previous commit | 回退 |

## Scope 范围

| Scope | Description |
|-------|-------------|
| data | 数据模块 |
| plotting | 可视化模块 |
| stats | 统计模块 |
| ml | 机器学习模块 |
| utils | 工具模块 |
| cli | 命令行工具 |
| tests | 测试模块 |
| docs | 文档 |
| examples | 示例 |
| config | 配置 |
| benchmark | 性能测试 |
| all | 多个模块或全局 |

## Examples 示例

```
feat(data): 添加CSV文件自动检测功能

- 支持逗号分隔和制表符分隔
- 自动检测文件编码
- 添加错误处理

Closes #123
```

```
fix(plots): 修复热力图中文字体显示问题

- 添加中文字体配置
- 使用SimHei字体
- 添加unicode_minus配置

Related: #456
```

```
docs: 添加英文版使用文档

- 新增README.en.md
- 新增USAGE.en.md
- 新增UV_SETUP.en.md
```

```
test(plotting): 添加可视化模块测试

- 添加Plotter类测试
- 添加辅助函数测试
- 覆盖12+测试用例
```

## Rules 规则

1. **主题行不超过50个字符**
2. **使用祈使语气**："Add" not "Added"
3. **不要以句号结尾**
4. **主题行小写**
5. **正文每行不超过72个字符**
6. **在正文和主题之间空一行**
7. **使用正文解释what和why，不解释how**

## Commit Message Example 完整示例

```
feat(data): 添加DataLoader多格式加载支持

新增DataLoader类，支持自动检测和加载多种数据格式：
- CSV/TSV文件
- Excel文件 (.xlsx, .xls)
- JSON文件
- Parquet文件
- Feather文件

所有方法都支持pandas和polars双引擎。

BREAKING CHANGE: load()方法签名变更
Closes #10
Closes #25
```
