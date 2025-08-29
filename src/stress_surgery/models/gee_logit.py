"""Cluster-robust logistic regression via GEE."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import statsmodels.api as sm


def fit(df: pd.DataFrame, seed: int = 42) -> Dict[str, float]:
    y = df["success_primary"]
    X = sm.add_constant(df[["exposure_index"]])
    groups = df.get("facility_id", pd.Series(0, index=df.index))
    model = sm.GEE(y, X, groups=groups, family=sm.families.Binomial()).fit()
    return {"coef_exposure_index": float(model.params["exposure_index"])}
