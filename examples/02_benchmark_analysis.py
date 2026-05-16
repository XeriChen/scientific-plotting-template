"""
示例2: 性能测试分析
==================

展示如何使用scientific_template进行性能测试数据分析。

运行方式:
    python examples/02_benchmark_analysis.py
"""

from scientific_template import Plotter, StatisticalAnalyzer, load_config, ensure_dir
import pandas as pd
import numpy as np
import os

def analyze_benchmark_results():
    """分析SSE模拟器的性能测试结果"""
    
    print("=== Performance Benchmark Analysis ===")
    
    # 设置样式
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['savefig.dpi'] = 300
    
    # 尝试加载配置文件
    try:
        config = load_config("config.yaml")
    except FileNotFoundError:
        print("Warning: config.yaml not found, using default configuration")
        config = None
    
    # 加载性能数据
    benchmark_data_path = "benchmark_results/benchmark_data.csv"
    if not os.path.exists(benchmark_data_path):
        print(f"Error: Benchmark data not found at {benchmark_data_path}")
        print("Please run the benchmark first: python benchmark_simple.py")
        return
    
    df = pd.read_csv(benchmark_data_path)
    print(f"Loaded {len(df)} benchmark records")
    
    # 创建Plotter
    plotter = Plotter(style="seaborn-v0_8", context="paper")
    output_dir = ensure_dir("benchmark_results")
    
    # 1. 线程扩展性分析
    thread_data = df[df['diag'] == 'sharemem']
    if not thread_data.empty:
        thread_summary = thread_data.groupby(['sites', 'threads']).agg({
            'execution_time': 'mean',
            'updates_per_sec': 'mean'
        }).reset_index()
        
        # 绘制线程扩展性图
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1 = axes[0]
        available_sites = sorted(thread_summary['sites'].unique())[:3]
        for sites in available_sites:
            subset = thread_summary[thread_summary['sites'] == sites]
            ax1.plot(subset['threads'], subset['execution_time'], 
                     marker='o', label=f'{sites} sites')
        ax1.set_xlabel('Thread Count')
        ax1.set_ylabel('Execution Time (s)')
        ax1.set_title('Thread Scaling Performance')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2 = axes[1]
        for sites in available_sites:
            subset = thread_summary[thread_summary['sites'] == sites]
            baseline = subset[subset['threads'] == 1]['execution_time'].values[0]
            speedup = baseline / subset['execution_time']
            ax2.plot(subset['threads'], speedup, marker='s', label=f'{sites} sites')
        ax2.plot([1, 4], [1, 4], 'k--', alpha=0.5, label='Ideal')
        ax2.set_xlabel('Thread Count')
        ax2.set_ylabel('Speedup')
        ax2.set_title('Thread Scaling Speedup')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plotter.save_figure(fig, output_dir / "thread_scaling.png")
        print("Saved: thread_scaling.png")
    else:
        print("Warning: No sharemem data found for thread scaling analysis")
    
    # 2. 策略对比分析
    strategy_data = df.groupby(['diag', 'offdiag']).agg({
        'execution_time': 'mean',
        'updates_per_sec': 'mean'
    }).reset_index()
    strategy_data['strategy'] = strategy_data['diag'] + '+' + strategy_data['offdiag']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(strategy_data['strategy'], strategy_data['execution_time'])
    ax.set_xlabel('Update Strategy')
    ax.set_ylabel('Execution Time (s)')
    ax.set_title('Strategy Comparison')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plotter.save_figure(fig, output_dir / "strategy_comparison.png")
    print("Saved: strategy_comparison.png")
    
    # 3. 统计分析
    analyzer = StatisticalAnalyzer()
    stats = analyzer.descriptive_stats(df[['execution_time', 'updates_per_sec']])
    print("\n=== Performance Statistics ===")
    print(stats)
    
    # 4. 相关性分析
    numeric_cols = ['sites', 'threads', 'execution_time', 'updates_per_sec']
    corr_matrix = analyzer.correlation(df[numeric_cols])
    fig = plotter.create_heatmap(corr_matrix, annot=True, title="Feature Correlations")
    plotter.save_figure(fig, output_dir / "correlation_heatmap.png")
    print("Saved: correlation_heatmap.png")
    
    # 5. 规模扩展性分析
    size_data = df.groupby('sites').agg({
        'execution_time': 'mean',
        'updates_per_sec': 'mean'
    }).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(size_data['sites'], size_data['execution_time'], 'b-o', label='Execution Time')
    ax.set_xlabel('Lattice Sites')
    ax.set_ylabel('Execution Time (s)', color='b')
    ax.set_title('Size Scaling Performance')
    
    ax2 = ax.twinx()
    ax2.plot(size_data['sites'], size_data['updates_per_sec'], 'r-s', label='Updates/sec')
    ax2.set_ylabel('Updates per Second', color='r')
    
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.tight_layout()
    plotter.save_figure(fig, output_dir / "size_scaling.png")
    print("Saved: size_scaling.png")
    
    print("\n=== Analysis Complete ===")
    print(f"All charts saved to: {os.path.abspath('benchmark_results')}")

if __name__ == "__main__":
    analyze_benchmark_results()
