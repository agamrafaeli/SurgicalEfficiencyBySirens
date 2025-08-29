"""Exposure-response curve utilities (placeholder)."""
from __future__ import annotations

import pandas as pd


def stress_curve(df: pd.DataFrame) -> pd.Series:
    """Return mean success by exposure decile."""
    df = df.copy()
    df["decile"] = pd.qcut(df["exposure_index"], 10, labels=False, duplicates="drop")
    return df.groupby("decile")["success_primary"].mean()
