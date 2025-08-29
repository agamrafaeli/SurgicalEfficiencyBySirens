"""Cox proportional hazards model placeholder."""
from __future__ import annotations

from typing import Dict

import pandas as pd
from lifelines import CoxPHFitter


def fit(df: pd.DataFrame, seed: int = 42) -> Dict[str, float]:
    if not {"time", "event", "exposure_index"}.issubset(df.columns):
        return {}
    cph = CoxPHFitter()
    cph.fit(df[["time", "event", "exposure_index"]], duration_col="time", event_col="event")
    return {"coef_exposure_index": float(cph.params_["exposure_index"])}
