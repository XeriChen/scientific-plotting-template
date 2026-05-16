"""
Simplified SSE Benchmark Script
"""

import subprocess
import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_sim(sites, updates, threads, diag, offdiag):
    time_file = OUTPUT_DIR / f"temp_{os.getpid()}.txt"
    cmd = [
        SSE_EXECUTABLE,
        "--sites", str(sites),
        "--updates", str(updates),
        "--threads", str(threads),
        "--diag", diag,
        "--offdiag", offdiag,
        "--seed", "139711",
        "--time-file", str(time_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    exec_time = None
    if time_file.exists():
        with open(time_file) as f:
            lines = f.readlines()
            if lines:
                try:
                    exec_time = float(lines[-1].strip())
                except:
                    pass
        time_file.unlink()

    total_updates = updates * 4
    return {
        "sites": sites,
        "updates": updates,
        "threads": threads,
        "diag": diag,
        "offdiag": offdiag,
        "execution_time": exec_time,
        "total_updates": total_updates,
        "updates_per_sec": total_updates / exec_time if exec_time else 0,
        "time_per_update_ms": (exec_time / total_updates * 1000) if exec_time else 0
    }


def main():
    print("="*80)
    print("SSE Quantum Monte Carlo Simulator - Performance Benchmark")
    print("="*80)

    results = []

    # Thread scaling test
    print("\n=== Thread Scaling Test ===")
    for sites in [16, 32, 64]:
        for threads in [1, 2, 4]:
            print(f"Testing: sites={sites}, threads={threads}", end=" ")
            result = run_sim(sites, 3000, threads, "sharemem", "lineupdatethread")
            results.append(result)
            print(f"-> {result['execution_time']:.3f}s")

    # Strategy comparison
    print("\n=== Strategy Comparison ===")
    strategies = [
        ("singlecpu", "lineupdate"),
        ("sharemem", "lineupdate"),
        ("sharemem", "lineupdatethread"),
        ("sharemem", "sharelineupdate"),
    ]
    for diag, offdiag in strategies:
        print(f"Testing: {diag}+{offdiag}", end=" ")
        result = run_sim(32, 3000, 4, diag, offdiag)
        results.append(result)
        print(f"-> {result['execution_time']:.3f}s")

    # Size scaling
    print("\n=== Size Scaling Test ===")
    for sites in [8, 16, 32, 64]:
        print(f"Testing: sites={sites}", end=" ")
        result = run_sim(sites, 3000, 4, "sharemem", "lineupdatethread")
        results.append(result)
        print(f"-> {result['execution_time']:.3f}s")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_DIR / "benchmark_data.csv", index=False)
    print(f"\nData saved to: {OUTPUT_DIR / 'benchmark_data.csv'}")

    # Calculate speedup
    baseline = df[df['threads'] == 1].groupby('sites')['execution_time'].mean()
    df['speedup'] = df.apply(
        lambda r: baseline.get(r['sites'], r['execution_time']) / r['execution_time']
        if r['execution_time'] and r['threads'] == 1 else 1.0, axis=1
    )

    # Create visualizations
    print("\n=== Generating Visualizations ===")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['savefig.dpi'] = 300
    sns.set_style("whitegrid")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Thread scaling
    ax1 = axes[0, 0]
    for sites in [16, 32, 64]:
        subset = df[(df['sites'] == sites) & (df['threads'].isin([1, 2, 4]))]
        subset = subset.groupby('threads')['execution_time'].mean().reset_index()
        ax1.plot(subset['threads'], subset['execution_time'], marker='o', label=f'Sites={sites}')
    ax1.set_xlabel('Thread Count')
    ax1.set_ylabel('Execution Time (s)')
    ax1.set_title('Thread Scaling: Execution Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Speedup
    ax2 = axes[0, 1]
    for sites in [16, 32, 64]:
        subset = df[(df['sites'] == sites) & (df['threads'].isin([1, 2, 4]))]
        subset = subset.groupby('threads')['speedup'].mean().reset_index()
        ax2.plot(subset['threads'], subset['speedup'], marker='s', label=f'Sites={sites}')
    ax2.plot([1, 4], [1, 4], 'k--', alpha=0.5, label='Ideal')
    ax2.set_xlabel('Thread Count')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Thread Scaling: Speedup')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Strategy comparison
    ax3 = axes[1, 0]
    strategy_data = df.groupby(['diag', 'offdiag'])['execution_time'].mean().reset_index()
    strategy_data['strategy'] = strategy_data['diag'] + '+' + strategy_data['offdiag']
    bars = ax3.bar(range(len(strategy_data)), strategy_data['execution_time'])
    ax3.set_xticks(range(len(strategy_data)))
    ax3.set_xticklabels(strategy_data['strategy'], rotation=45, ha='right')
    ax3.set_ylabel('Execution Time (s)')
    ax3.set_title('Strategy Comparison')
    ax3.grid(True, alpha=0.3, axis='y')

    # Plot 4: Size scaling
    ax4 = axes[1, 1]
    size_data = df.groupby('sites')['execution_time'].mean().reset_index()
    ax4.plot(size_data['sites'], size_data['execution_time'], 'b-o')
    ax4.set_xlabel('Lattice Sites')
    ax4.set_ylabel('Execution Time (s)')
    ax4.set_title('Size Scaling')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "benchmark_overview.png", dpi=300, bbox_inches='tight')
    print(f"  Saved: benchmark_overview.png")

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot = df.pivot_table(index='sites', columns='threads', values='execution_time')
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='viridis_r', ax=ax)
    ax.set_title('Performance Heatmap: Execution Time (s)')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "performance_heatmap.png", dpi=300, bbox_inches='tight')
    print(f"  Saved: performance_heatmap.png")

    # Generate tables
    print("\n=== Performance Summary Tables ===")

    print("\n1. Thread Scaling Summary:")
    thread_summary = df[df['threads'].isin([1, 2, 4])].groupby('threads').agg({
        'execution_time': ['mean', 'std'],
        'speedup': 'mean'
    }).round(4)
    print(thread_summary.to_string())

    print("\n2. Strategy Comparison:")
    strategy_summary = df.groupby(['diag', 'offdiag']).agg({
        'execution_time': ['mean', 'std']
    }).round(4)
    print(strategy_summary.to_string())

    print("\n3. Size Scaling:")
    size_summary = df.groupby('sites').agg({
        'execution_time': 'mean',
        'updates_per_sec': 'mean'
    }).round(2)
    print(size_summary.to_string())

    thread_summary.to_csv(OUTPUT_DIR / "thread_summary.csv")
    strategy_summary.to_csv(OUTPUT_DIR / "strategy_summary.csv")
    size_summary.to_csv(OUTPUT_DIR / "size_summary.csv")

    print("\n" + "="*80)
    print("BENCHMARK COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
