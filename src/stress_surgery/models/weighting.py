"""Propensity weighting placeholder."""
from __future__ import annotations

from typing import Dict

import pandas as pd
from sklearn.linear_model import LogisticRegression


def fit(df: pd.DataFrame, seed: int = 42) -> Dict[str, float]:
    X = df[["exposure_index"]]
    y = df["siren_during_case"]
    model = LogisticRegression().fit(X, y)
    return {"coef_exposure_index": float(model.coef_[0, 0])}
