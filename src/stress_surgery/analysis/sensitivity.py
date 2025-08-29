"""Sensitivity analyses (placeholder)."""
from __future__ import annotations

import pandas as pd


def placebo_shift(df: pd.DataFrame, minutes: int) -> pd.DataFrame:
    """Shift siren times by given minutes for placebo test."""
    df = df.copy()
    df["siren_recency_min"] = df["siren_recency_min"] + minutes
    return df
