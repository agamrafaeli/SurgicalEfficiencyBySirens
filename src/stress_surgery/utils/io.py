"""I/O utilities for CSV and Parquet with minimal dtype handling."""
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def read_csv(path: Path, dtype: Optional[Dict[str, str]] = None, **kwargs) -> pd.DataFrame:
    """Read a CSV file with optional dtype mapping."""
    return pd.read_csv(path, dtype=dtype, **kwargs)


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    """Write DataFrame to Parquet ensuring parent directory exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
