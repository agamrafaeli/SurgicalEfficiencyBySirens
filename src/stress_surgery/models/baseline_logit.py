"""Baseline logistic regression model for complication outcomes."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import statsmodels.api as sm


def fit(
    df: pd.DataFrame,
    seed: int = 42,
    outcome: str = "complication_intraop",
) -> Dict[str, float]:
    """Fit logistic regression of complication on exposure index.

    Parameters
    ----------
    df : DataFrame
        Feature table containing complication indicator and `exposure_index`.
    seed : int
        Random seed (unused but kept for API compatibility).
    outcome : str
        Column name of complication outcome (e.g., `complication_intraop`,
        `complication_short_term`, `complication_long_term`).
    """
    if outcome not in df.columns:
        raise KeyError(f"Outcome column '{outcome}' not in DataFrame")
    y = df[outcome]
    X = sm.add_constant(df[["exposure_index"]])
    try:
        model = sm.Logit(y, X).fit(disp=0)
        coef = float(model.params["exposure_index"])
    except Exception:
        # Fallback for tiny/singular cases: use regularized fit
        model = sm.Logit(y, X).fit_regularized(alpha=1e-6, L1_wt=0.0)
        coef = float(model.params["exposure_index"]) if "exposure_index" in model.params else float(model.params[1])
    return {"coef_exposure_index": coef}
