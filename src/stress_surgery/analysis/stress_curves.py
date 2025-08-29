"""Exposure-response curve utilities (placeholder)."""
from __future__ import annotations

import pandas as pd


def stress_curve(df: pd.DataFrame, outcome: str = "complication_intraop") -> pd.Series:
    """Return mean complication rate by exposure decile.

    Parameters
    ----------
    df : DataFrame with `exposure_index` and a complication outcome column.
    outcome : Column name of complication indicator to aggregate.
    """
    df = df.copy()
    if outcome not in df.columns:
        raise KeyError(f"Outcome column '{outcome}' not in DataFrame")
    df["decile"] = pd.qcut(df["exposure_index"], 10, labels=False, duplicates="drop")
    return df.groupby("decile")[outcome].mean()
