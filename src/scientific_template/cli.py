"""
Command Line Interface for Scientific Template
==============================================

A CLI tool for data analysis and visualization workflows.
"""

import click
from pathlib import Path
import json


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Scientific Template - A modern Python data analysis workspace."""
    pass


@main.command()
@click.option("--name", default="World", help="Name to greet.")
def hello(name):
    """Greet a user."""
    click.echo(f"Hello, {name}!")


@main.command()
@click.option("--input-file", "-i", required=True, type=Path, help="Input data file")
@click.option("--output-file", "-o", type=Path, help="Output file (optional)")
@click.option("--format", "-f", "file_format", default=None, help="File format")
def info(input_file, output_file, file_format):
    """Display information about a data file."""
    from scientific_template.data import DataLoader
    
    loader = DataLoader()
    try:
        df = loader.load(input_file, file_format=file_format)
        click.echo(f"\n📊 Data File Information: {input_file}")
        click.echo("=" * 50)
        click.echo(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        click.echo(f"\nColumns:")
        for col in df.columns:
            click.echo(f"  - {col}")
        click.echo(f"\nData Types:")
        if hasattr(df, 'dtypes'):
            for col, dtype in df.dtypes.items():
                click.echo(f"  - {col}: {dtype}")
    except Exception as e:
        click.echo(f"❌ Error loading file: {e}", err=True)


@main.command()
@click.option("--style", "-s", default="seaborn-v0_8", help="Plotting style")
@click.option("--context", "-c", default="notebook", help="Plotting context")
def config_style(style, context):
    """Configure plotting style."""
    from scientific_template.utils import set_style
    
    set_style(style, context)
    click.echo(f"✅ Plotting style set to '{style}' with context '{context}'")


@main.command()
@click.option("--config-file", "-c", type=Path, help="Configuration file")
@click.option("--key", "-k", help="Configuration key to get")
def config_get(config_file, key):
    """Get configuration values."""
    from scientific_template.utils import load_config
    
    if not config_file:
        click.echo("❌ Please provide a configuration file", err=True)
        return
    
    try:
        config = load_config(config_file)
        if key:
            keys = key.split('.')
            value = config
            for k in keys:
                value = value[k]
            click.echo(json.dumps(value, indent=2))
        else:
            click.echo(json.dumps(config, indent=2))
    except Exception as e:
        click.echo(f"❌ Error loading config: {e}", err=True)


@main.command()
@click.argument("config_data")
@click.option("--output-file", "-o", required=True, type=Path, help="Output config file")
def config_save(config_data, output_file):
    """Save configuration to a file."""
    from scientific_template.utils import save_config
    
    try:
        config = json.loads(config_data)
        save_config(config, output_file)
        click.echo(f"✅ Configuration saved to {output_file}")
    except json.JSONDecodeError as e:
        click.echo(f"❌ Invalid JSON: {e}", err=True)
    except Exception as e:
        click.echo(f"❌ Error saving config: {e}", err=True)


@main.command()
def init():
    """Initialize a new scientific template project."""
    from scientific_template.utils import ensure_dir
    
    directories = ["data", "notebooks", "examples", "tests", "docs", "output"]
    
    click.echo("🚀 Initializing scientific template project...")
    for dir_name in directories:
        path = ensure_dir(Path(dir_name))
        click.echo(f"  ✓ Created directory: {path}")
    
    # Create a sample config file
    config_path = Path("config.yaml")
    if not config_path.exists():
        from scientific_template.utils import save_config
        save_config({
            "project": {
                "name": "My Scientific Project",
                "version": "0.1.0"
            },
            "data": {
                "input_dir": "data/input",
                "output_dir": "data/output"
            },
            "plotting": {
                "style": "seaborn-v0_8",
                "context": "notebook",
                "dpi": 300
            }
        }, config_path)
        click.echo(f"  ✓ Created sample config: {config_path}")
    
    click.echo("\n✅ Project initialization complete!")
    click.echo("\nNext steps:")
    click.echo("  1. Add your data to the data/ directory")
    click.echo("  2. Edit config.yaml with your settings")
    click.echo("  3. Start analyzing in notebooks/")


if __name__ == "__main__":
    main()
