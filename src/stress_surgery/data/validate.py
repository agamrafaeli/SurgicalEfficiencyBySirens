"""Input data validation using pandera."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import pandera as pa

from .schema import get_schema, SCHEMAS
from ..utils import io


def validate_file(path: Path, schema: pa.DataFrameSchema) -> Dict[str, int]:
    """Validate a single CSV file, returning summary stats."""
    df = io.read_csv(path)
    schema.validate(df, lazy=True)
    return {"rows": len(df), "columns": len(df.columns)}


def validate_directory(data_dir: Path) -> None:
    """Validate all known CSVs in a directory and print summary."""
    summary = {}
    for name, schema in SCHEMAS.items():
        path = data_dir / f"{name}.csv"
        if not path.exists():
            continue
        try:
            summary[name] = validate_file(path, schema)
        except pa.errors.SchemaErrors as exc:  # pragma: no cover - error path
            raise SystemExit(f"Validation failed for {name}: {exc.failure_cases}")
    typer_echo = __import__("typer").echo
    typer_echo(json.dumps(summary))
