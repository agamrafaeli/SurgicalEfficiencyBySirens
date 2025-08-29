"""Difference-in-differences placeholder implementation."""
from __future__ import annotations

from typing import Dict

import pandas as pd


def fit(df: pd.DataFrame, seed: int = 42) -> Dict[str, float]:
    """Return zero ATT for placeholder."""
    return {"att": 0.0}
