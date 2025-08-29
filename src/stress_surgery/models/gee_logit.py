"""Cluster-robust logistic regression via GEE for complication outcomes."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import statsmodels.api as sm


def fit(df: pd.DataFrame, seed: int = 42, outcome: str = "complication_intraop") -> Dict[str, float]:
    if outcome not in df.columns:
        raise KeyError(f"Outcome column '{outcome}' not in DataFrame")
    y = df[outcome]
    X = sm.add_constant(df[["exposure_index"]])
    groups = df.get("facility_id", pd.Series(0, index=df.index))
    model = sm.GEE(y, X, groups=groups, family=sm.families.Binomial()).fit()
    return {"coef_exposure_index": float(model.params["exposure_index"])}
