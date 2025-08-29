"""Command line interface for stress_surgery.

Example usage:

    stress-surgery validate --data-dir data/raw
"""
from pathlib import Path
from typing import Optional

import pandas as pd
import typer

from .data import features as feature_mod
from .data import validate as validate_mod
from .analysis import eda as eda_mod
from .models import baseline_logit, gee_logit, did, cox_survival, weighting
from .reporting import build_report

app = typer.Typer(help="Tools for analysing surgical outcomes under siren stress")


@app.command()
def validate(data_dir: Path = typer.Option(..., help="Directory with raw CSV files")) -> None:
    """Run pandera validation on raw CSVs."""
    validate_mod.validate_directory(data_dir)


@app.command("build-features")
def build_features(
    data_dir: Path = typer.Option(..., help="Directory with raw CSV files"),
    out: Path = typer.Option(..., help="Output Parquet file"),
    config: Path = typer.Option(..., help="YAML config file"),
) -> None:
    """Create model-ready features and save to Parquet."""
    df = feature_mod.build_features(data_dir, config)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out)


@app.command()
def eda(
    features: Path = typer.Option(..., help="Parquet file with features"),
    out: Path = typer.Option(..., help="Directory for figures"),
) -> None:
    """Generate exploratory plots."""
    df = pd.read_parquet(features)
    out.mkdir(parents=True, exist_ok=True)
    eda_mod.run_eda(df, out)


@app.command()
def train(
    features: Path = typer.Option(..., help="Parquet file"),
    model: str = typer.Option("baseline", help="Model type"),
    seed: int = typer.Option(42, help="Random seed"),
) -> None:
    """Train a model on features."""
    df = pd.read_parquet(features)
    if model == "baseline":
        baseline_logit.fit(df, seed)
    elif model == "gee":
        gee_logit.fit(df, seed)
    elif model == "did":
        did.fit(df, seed)
    elif model == "cox":
        cox_survival.fit(df, seed)
    elif model == "weighting":
        weighting.fit(df, seed)
    else:
        raise typer.BadParameter(f"Unknown model {model}")


@app.command()
def evaluate(
    features: Path = typer.Option(...),
    model: str = typer.Option("baseline"),
    out: Path = typer.Option(..., help="Output metrics JSON"),
    seed: int = typer.Option(42),
) -> None:
    """Evaluate a fitted model and write metrics."""
    df = pd.read_parquet(features)
    result = baseline_logit.fit(df, seed) if model == "baseline" else {}
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.Series(result).to_json(out)


@app.command()
def report(
    features: Path = typer.Option(...),
    model: str = typer.Option("baseline"),
    template: Path = typer.Option(...),
    out: Path = typer.Option(...),
) -> None:
    """Build HTML report using Jinja2 template."""
    df = pd.read_parquet(features)
    ctx = {"n_obs": len(df), "model": model}
    out.parent.mkdir(parents=True, exist_ok=True)
    build_report.render_report(template, out, ctx)


@app.command()
def simulate(
    features: Path = typer.Option(...),
    what_if: str = typer.Option(..., help="Expression to adjust a column, e.g. 'reduce disruption_score by 2'"),
) -> None:
    """Run simple scenario analysis adjusting selected covariates."""
    df = pd.read_parquet(features)
    col = what_if.split()[1]
    delta = float(what_if.split()[-1])
    if "reduce" in what_if:
        df[col] = df[col] - delta
    else:
        df[col] = df[col] + delta
    typer.echo(df.head())


if __name__ == "__main__":  # pragma: no cover
    app()
