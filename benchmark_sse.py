"""
SSE Quantum Monte Carlo Simulator Benchmark Script
=================================================

This script performs comprehensive performance testing on the SSE simulator
and generates visualizations using the scientific-plotting-template.
"""

import subprocess
import csv
import time
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from scientific_template.plotting import Plotter
    from scientific_template.stats import StatisticalAnalyzer
    USE_SCIENTIFIC_TEMPLATE = True
except ImportError:
    USE_SCIENTIFIC_TEMPLATE = False
    class Plotter:
        @staticmethod
        def set_style(style="seaborn-v0_8", context="notebook"):
            sns.set_style(style)
            sns.set_context(context)
            plt.rcParams['figure.figsize'] = (10, 6)
            plt.rcParams['figure.dpi'] = 100
            plt.rcParams['savefig.dpi'] = 300
        
        @staticmethod
        def save_figure(fig, path):
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(path, dpi=300, bbox_inches='tight')


def find_sse_executable():
    """查找 SSE 可执行文件，支持从环境变量、默认位置或 PATH 中查找"""
    # 1. 从环境变量查找
    exe_path = os.environ.get("SSE_EXECUTABLE")
    if exe_path and os.path.exists(exe_path):
        return exe_path
    
    # 2. 从默认位置查找
    default_paths = [
        Path.home() / "Documents" / "cqu-bysj-phy" / "src" / "build" / "src" / "SSE",
        Path(__file__).parent.parent / "cqu-bysj-phy" / "src" / "build" / "src" / "SSE",
        Path(__file__).parent / "SSE",
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            return str(path)
    
    # 3. 检查是否在 PATH 中
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        exe_in_path = Path(path_dir) / "SSE"
        if exe_in_path.exists():
            return str(exe_in_path)
    
    return "SSE"  # 默认，尝试直接调用


SSE_EXECUTABLE = find_sse_executable()

# 验证可执行文件是否存在
if not (os.path.exists(SSE_EXECUTABLE) or os.access(SSE_EXECUTABLE, os.X_OK) or 
         any((Path(path_dir) / "SSE").exists() for path_dir in os.environ.get("PATH", "").split(os.pathsep))):
    print("警告: 找不到 SSE 可执行文件", file=sys.stderr)
    print(f"请设置环境变量 SSE_EXECUTABLE=/path/to/SSE 或将 SSE 添加到 PATH", file=sys.stderr)

OUTPUT_DIR = Path(__file__).parent / "benchmark_results"
DATA_FILE = OUTPUT_DIR / "benchmark_data.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DIAGONAL_TYPES = ["singlecpu", "sharemem"]
OFF_DIAGONAL_TYPES = ["lineupdate", "sharelineupdate", "lineupdateptr", "lineupdatethread"]
THREAD_COUNTS = [1, 2, 4, 8]
SITE_COUNTS = [16, 32, 64, 128]
UPDATE_COUNT = 5000
NUM_RUNS = 3


def run_simulation(
    sites: int,
    updates: int,
    threads: int,
    diag: str,
    offdiag: str,
    seed: int = 139711,
    time_file: str = None
) -> Dict:
    """Run a single SSE simulation and return performance metrics."""
    if time_file is None:
        time_file = str(OUTPUT_DIR / f"temp_time_{os.getpid()}.txt")

    cmd = [
        SSE_EXECUTABLE,
        "--sites", str(sites),
        "--updates", str(updates),
        "--threads", str(threads),
        "--diag", diag,
        "--offdiag", offdiag,
        "--seed", str(seed),
        "--time-file", time_file
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        exec_time = None
        if os.path.exists(time_file):
            with open(time_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    try:
                        exec_time = float(lines[-1].strip())
                    except ValueError:
                        pass
            os.remove(time_file)

        total_updates = updates * 4
        updates_per_sec = (total_updates / exec_time) if exec_time and exec_time > 0 else 0
        time_per_update = (exec_time / total_updates * 1000) if exec_time and exec_time > 0 else 0

        return {
            "sites": sites,
            "updates": updates,
            "threads": threads,
            "diag": diag,
            "offdiag": offdiag,
            "execution_time": exec_time,
            "total_updates": total_updates,
            "updates_per_sec": updates_per_sec,
            "time_per_update_ms": time_per_update,
            "seed": seed,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "sites": sites,
            "updates": updates,
            "threads": threads,
            "diag": diag,
            "offdiag": offdiag,
            "execution_time": None,
            "total_updates": total_updates,
            "updates_per_sec": 0,
            "time_per_update_ms": 0,
            "seed": seed,
            "success": False
        }
    except Exception as e:
        print(f"Error running simulation: {e}")
        return None


def run_thread_scaling_benchmark() -> List[Dict]:
    """Scenario A: Test thread count impact on performance."""
    print("\n=== Running Thread Scaling Benchmark ===")
    results = []

    for sites in SITE_COUNTS:
        for threads in THREAD_COUNTS:
            for run in range(NUM_RUNS):
                print(f"  Sites={sites}, Threads={threads}, Run={run+1}/{NUM_RUNS}", end=" ")
                result = run_simulation(
                    sites=sites,
                    updates=UPDATE_COUNT,
                    threads=threads,
                    diag="sharemem",
                    offdiag="lineupdatethread",
                    seed=139711 + run
                )
                if result:
                    results.append(result)
                    print(f"-> {result['execution_time']:.3f}s")
                else:
                    print("-> FAILED")

    return results


def run_strategy_comparison_benchmark() -> List[Dict]:
    """Scenario B: Compare different update strategies."""
    print("\n=== Running Strategy Comparison Benchmark ===")
    results = []

    test_sites = [16, 32, 64]
    threads = 4

    strategy_pairs = [
        ("singlecpu", "lineupdate"),
        ("sharemem", "lineupdate"),
        ("sharemem", "lineupdatethread"),
        ("sharemem", "sharelineupdate"),
        ("sharemem", "lineupdateptr"),
    ]

    for sites in test_sites:
        for diag, offdiag in strategy_pairs:
            for run in range(NUM_RUNS):
                print(f"  Sites={sites}, Strategy={diag}+{offdiag}, Run={run+1}/{NUM_RUNS}", end=" ")
                result = run_simulation(
                    sites=sites,
                    updates=UPDATE_COUNT,
                    threads=threads,
                    diag=diag,
                    offdiag=offdiag,
                    seed=139711 + run
                )
                if result:
                    results.append(result)
                    print(f"-> {result['execution_time']:.3f}s")
                else:
                    print("-> FAILED")

    return results


def run_size_scaling_benchmark() -> List[Dict]:
    """Scenario C: Test performance scaling with lattice size."""
    print("\n=== Running Size Scaling Benchmark ===")
    results = []

    large_sites = [8, 16, 32, 64, 128, 256]
    threads = 4

    for sites in large_sites:
        for run in range(NUM_RUNS):
            print(f"  Sites={sites}, Run={run+1}/{NUM_RUNS}", end=" ")
            result = run_simulation(
                sites=sites,
                updates=UPDATE_COUNT,
                threads=threads,
                diag="sharemem",
                offdiag="lineupdatethread",
                seed=139711 + run
            )
            if result:
                results.append(result)
                print(f"-> {result['execution_time']:.3f}s")
            else:
                print("-> FAILED")

    return results


def save_results(results: List[Dict], filename: str = None):
    """Save benchmark results to CSV file."""
    if not results:
        print("No results to save!")
        return

    if filename is None:
        filename = DATA_FILE

    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"\nResults saved to: {filename}")
    print(f"Total records: {len(df)}")
    return df


def calculate_speedup(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate speedup relative to single-thread performance."""
    df = df.copy()

    baseline = df[(df['threads'] == 1)].groupby(['sites', 'diag', 'offdiag'])['execution_time'].mean()
    df['speedup'] = 1.0

    for idx, row in df.iterrows():
        key = (row['sites'], row['diag'], row['offdiag'])
        if key in baseline.index and baseline[key] > 0:
            baseline_time = baseline[key]
            df.at[idx, 'speedup'] = baseline_time / row['execution_time'] if row['execution_time'] else 0

    return df


def create_visualizations(df: pd.DataFrame):
    """Generate performance visualization charts."""
    print("\n=== Generating Visualizations ===")

    plotter = Plotter(style="seaborn-v0_8", context="paper")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['savefig.dpi'] = 300

    df_successful = df[df['success'] == True].copy()

    avg_data = df_successful.groupby(['sites', 'threads']).agg({
        'execution_time': 'mean',
        'updates_per_sec': 'mean',
        'speedup': 'mean'
    }).reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax1 = axes[0, 0]
    for sites in df_successful['sites'].unique():
        subset = avg_data[avg_data['sites'] == sites]
        ax1.plot(subset['threads'], subset['execution_time'],
                marker='o', label=f'Sites={sites}')
    ax1.set_xlabel('Thread Count')
    ax1.set_ylabel('Execution Time (s)')
    ax1.set_title('Thread Scaling: Execution Time vs Threads')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = axes[0, 1]
    for sites in df_successful['sites'].unique():
        subset = avg_data[avg_data['sites'] == sites]
        ax2.plot(subset['threads'], subset['speedup'],
                marker='s', label=f'Sites={sites}')
    ax2.plot([1, max(df_successful['threads'])],
            [1, max(df_successful['threads'])],
            'k--', label='Ideal Scaling', alpha=0.5)
    ax2.set_xlabel('Thread Count')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Thread Scaling: Speedup vs Threads')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    strategy_data = df_successful.groupby(['sites', 'diag', 'offdiag']).agg({
        'execution_time': 'mean'
    }).reset_index()
    strategy_data['strategy'] = strategy_data['diag'] + '+' + strategy_data['offdiag']

    pivot_data = strategy_data[strategy_data['sites'].isin([16, 32, 64])].pivot_table(
        index='sites', columns='strategy', values='execution_time'
    )

    ax3 = axes[1, 0]
    pivot_data.plot(kind='bar', ax=ax3, width=0.8)
    ax3.set_xlabel('Lattice Sites')
    ax3.set_ylabel('Execution Time (s)')
    ax3.set_title('Strategy Comparison: Execution Time')
    ax3.legend(title='Strategy', bbox_to_anchor=(1.02, 1), loc='upper left')
    ax3.tick_params(axis='x', rotation=0)

    size_data = df_successful.groupby('sites').agg({
        'execution_time': 'mean',
        'updates_per_sec': 'mean'
    }).reset_index()

    ax4 = axes[1, 1]
    ax4_twin = ax4.twinx()
    ln1 = ax4.plot(size_data['sites'], size_data['execution_time'],
                  'b-o', label='Execution Time')
    ln2 = ax4_twin.plot(size_data['sites'], size_data['updates_per_sec'],
                       'r-s', label='Updates/sec')
    ax4.set_xlabel('Lattice Sites')
    ax4.set_ylabel('Execution Time (s)', color='b')
    ax4_twin.set_ylabel('Updates/sec', color='r')
    ax4.set_title('Size Scaling: Performance vs Lattice Size')
    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax4.legend(lns, labs, loc='upper left')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plotter.save_figure(fig, OUTPUT_DIR / "benchmark_overview.png")
    print(f"  Saved: benchmark_overview.png")

    fig_heat, ax = plt.subplots(figsize=(12, 8))
    heat_data = avg_data.pivot_table(
        index='sites', columns='threads', values='execution_time'
    )
    sns.heatmap(heat_data, annot=True, fmt='.2f', cmap='viridis_r', ax=ax)
    ax.set_title('Performance Heatmap: Execution Time (s)\n(Sites × Threads)')
    ax.set_xlabel('Thread Count')
    ax.set_ylabel('Lattice Sites')
    plotter.save_figure(fig_heat, OUTPUT_DIR / "performance_heatmap.png")
    print(f"  Saved: performance_heatmap.png")

    return df_successful


def generate_performance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Generate summary performance tables."""
    print("\n=== Generating Performance Tables ===")

    df_successful = df[df['success'] == True].copy()

    summary_stats = df_successful.groupby(['sites', 'threads']).agg({
        'execution_time': ['mean', 'std', 'min', 'max'],
        'updates_per_sec': 'mean',
        'speedup': 'mean'
    }).round(4)

    summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]
    summary_stats = summary_stats.reset_index()

    thread_summary = df_successful.groupby('threads').agg({
        'execution_time': ['mean', 'std'],
        'speedup': 'mean'
    }).round(4)
    thread_summary.columns = ['Avg_Time', 'Std_Time', 'Avg_Speedup']
    thread_summary = thread_summary.reset_index()

    strategy_summary = df_successful.groupby(['diag', 'offdiag']).agg({
        'execution_time': ['mean', 'std']
    }).round(4)
    strategy_summary.columns = ['Avg_Time', 'Std_Time']
    strategy_summary = strategy_summary.reset_index()

    summary_stats.to_csv(OUTPUT_DIR / "summary_statistics.csv", index=False)
    thread_summary.to_csv(OUTPUT_DIR / "thread_summary.csv", index=False)
    strategy_summary.to_csv(OUTPUT_DIR / "strategy_summary.csv", index=False)

    print(f"  Saved: summary_statistics.csv")
    print(f"  Saved: thread_summary.csv")
    print(f"  Saved: strategy_summary.csv")

    print("\n" + "="*80)
    print("THREAD SCALING SUMMARY")
    print("="*80)
    print(thread_summary.to_string(index=False))

    print("\n" + "="*80)
    print("STRATEGY COMPARISON SUMMARY")
    print("="*80)
    print(strategy_summary.to_string(index=False))

    return summary_stats, thread_summary, strategy_summary


def main():
    """Main benchmark execution function."""
    print("="*80)
    print("SSE Quantum Monte Carlo Simulator - Performance Benchmark")
    print("="*80)
    print(f"SSE Executable: {SSE_EXECUTABLE}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Update Count: {UPDATE_COUNT}")
    print(f"Number of Runs: {NUM_RUNS}")

    all_results = []

    results_a = run_thread_scaling_benchmark()
    all_results.extend(results_a)

    results_b = run_strategy_comparison_benchmark()
    all_results.extend(results_b)

    results_c = run_size_scaling_benchmark()
    all_results.extend(results_c)

    df = save_results(all_results)

    df = calculate_speedup(df)
    df.to_csv(DATA_FILE, index=False)

    create_visualizations(df)

    generate_performance_table(df)

    print("\n" + "="*80)
    print("BENCHMARK COMPLETE!")
    print("="*80)
    print(f"\nAll results saved to: {OUTPUT_DIR}")
    print("\nGenerated files:")
    print("  - benchmark_data.csv: Raw benchmark data")
    print("  - benchmark_results/benchmark_overview.png: Overview charts")
    print("  - benchmark_results/performance_heatmap.png: Performance heatmap")
    print("  - benchmark_results/summary_statistics.csv: Summary statistics")
    print("  - benchmark_results/thread_summary.csv: Thread scaling summary")
    print("  - benchmark_results/strategy_summary.csv: Strategy comparison summary")


if __name__ == "__main__":
    main()
