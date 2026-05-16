"""
示例1: 完整数据分析流程
=======================

展示如何使用scientific_template进行完整的数据分析流程。

运行方式:
    python examples/01_full_analysis.py
"""

from scientific_template import (
    DataLoader, DataProcessor, DataCleaner, DataTransformer,
    Plotter, StatisticalAnalyzer, ModelPipeline, CrossValidator,
    setup_logging, load_config, set_style, ensure_dir
)
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import os

def main():
    # 1. 初始化配置和日志
    logger = setup_logging(level="INFO", log_file="logs/analysis.log")
    
    # 尝试加载配置文件，如果不存在则使用默认值
    try:
        config = load_config("config.yaml")
        plot_style = config["plotting"]["style"]
        plot_context = config["plotting"]["context"]
        sample_data_path = config["data"]["sample_data"]
    except (FileNotFoundError, KeyError):
        logger.warning("config.yaml not found, using default configuration")
        plot_style = "seaborn-v0_8"
        plot_context = "notebook"
        sample_data_path = "data/input/sales_data.csv"
    
    logger.info("Starting analysis...")
    
    # 设置绘图风格
    set_style(style=plot_style, context=plot_context)
    
    # 2. 加载数据
    if not os.path.exists(sample_data_path):
        logger.error(f"Data file not found: {sample_data_path}")
        return
    
    loader = DataLoader(engine="pandas")
    df = loader.load_csv(sample_data_path)
    logger.info(f"Loaded {len(df)} records from {sample_data_path}")
    
    # 3. 数据清洗
    cleaner = DataCleaner(engine="pandas")
    df = cleaner.standardize_column_names(df, case="snake")
    df = cleaner.fix_data_types(df)
    
    # 4. 数据处理
    processor = DataProcessor(engine="pandas")
    df = processor.remove_duplicates(df)
    df = processor.handle_missing(df, strategy="fill_mean")
    
    # 5. 数据转换
    transformer = DataTransformer(engine="pandas")
    df = transformer.encode_categorical(df, columns=["category", "region"], method="onehot")
    
    # 6. 探索性分析
    analyzer = StatisticalAnalyzer()
    desc_stats = analyzer.descriptive_stats(df)
    logger.info("Descriptive statistics generated")
    print("\n=== Descriptive Statistics ===")
    print(desc_stats)
    
    # 7. 可视化
    plotter = Plotter()
    output_fig_dir = ensure_dir("output/figures")
    output_table_dir = ensure_dir("output/tables")
    
    # 创建图表
    fig1 = plotter.create_histogram(df, column="sales", title="Sales Distribution")
    plotter.save_figure(fig1, output_fig_dir / "sales_distribution.png")
    logger.info("Saved: sales_distribution.png")
    
    fig2 = plotter.create_bar_plot(df, x="category", y="sales", title="Sales by Category")
    plotter.save_figure(fig2, output_fig_dir / "sales_by_category.png")
    logger.info("Saved: sales_by_category.png")
    
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        fig3 = plotter.create_correlation_matrix(numeric_df)
        plotter.save_figure(fig3, output_fig_dir / "correlation_matrix.png")
        logger.info("Saved: correlation_matrix.png")
    
    logger.info("Visualizations saved")
    
    # 8. 机器学习建模
    X = df.drop(["sales", "date"], axis=1, errors="ignore")
    y = df["sales"]
    
    if len(X.columns) > 0:
        pipeline = ModelPipeline(model=RandomForestRegressor(n_estimators=100))
        results = pipeline.fit(X, y, test_size=0.2, random_state=42)
        
        logger.info(f"Model R²: {results['metrics']['r2']:.3f}")
        logger.info(f"Model RMSE: {results['metrics']['rmse']:.2f}")
        
        # 9. 交叉验证
        cv = CrossValidator(cv=5)
        cv_results = cv.validate(
            model=RandomForestRegressor(n_estimators=100),
            X=X, y=y,
            scoring="r2"
        )
        
        logger.info(f"CV R²: {cv_results['mean_score']:.3f} ± {cv_results['std_score']:.3f}")
    else:
        logger.warning("No features available for modeling")
    
    # 10. 保存结果
    desc_stats.to_csv(output_table_dir / "descriptive_stats.csv")
    logger.info("Saved: descriptive_stats.csv")
    
    logger.info("Analysis complete! Results saved to output/ directory")
    print("\n=== Analysis Complete ===")
    print(f"Output directory: {os.path.abspath('output')}")

if __name__ == "__main__":
    main()
