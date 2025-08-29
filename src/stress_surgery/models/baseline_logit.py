"""Baseline logistic regression model."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import statsmodels.api as sm


def fit(df: pd.DataFrame, seed: int = 42) -> Dict[str, float]:
    """Fit logistic regression of success on exposure index.

    Parameters
    ----------
    df : DataFrame
        Feature table containing `success_primary` and `exposure_index`.
    seed : int
        Random seed (unused but kept for API compatibility).
    """
    y = df["success_primary"]
    X = sm.add_constant(df[["exposure_index"]])
    model = sm.Logit(y, X).fit(disp=0)
    return {"coef_exposure_index": float(model.params["exposure_index"])}
