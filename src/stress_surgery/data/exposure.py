"""Compute siren exposure features for each surgical case."""
from __future__ import annotations

from datetime import timedelta
from typing import Tuple

import numpy as np
import pandas as pd

from ..utils.time import overlap_minutes


WINDOWS = {"6h": timedelta(hours=6), "24h": timedelta(hours=24)}


def _count_and_duration(sirens: pd.DataFrame, start: pd.Timestamp, window: timedelta) -> Tuple[int, float]:
    w_start = start - window
    mask = (sirens["siren_ts_end"] >= w_start) & (sirens["siren_ts_start"] <= start)
    subset = sirens[mask]
    count = len(subset)
    # Use a robust generator-based sum to avoid dtype issues on empty frames
    dur = sum(
        overlap_minutes(
            row.siren_ts_start.to_pydatetime(),
            row.siren_ts_end.to_pydatetime(),
            w_start.to_pydatetime(),
            start.to_pydatetime(),
        )
        for _, row in subset.iterrows()
    )
    return count, dur


def compute_exposure(ops: pd.DataFrame, sirens: pd.DataFrame) -> pd.DataFrame:
    """Return operations DataFrame with exposure features."""
    sirens = sirens.copy()
    sirens["siren_ts_start"] = pd.to_datetime(sirens["siren_ts_start"])
    sirens["siren_ts_end"] = pd.to_datetime(sirens["siren_ts_end"])

    feat_rows = []
    for _, op in ops.iterrows():
        start = pd.to_datetime(op.start_ts)
        end = pd.to_datetime(op.end_ts)
        fac = op.facility_id
        s_fac = sirens[sirens["facility_id"] == fac]
        counts = {}
        durations = {}
        for key, window in WINDOWS.items():
            c, d = _count_and_duration(s_fac, start, window)
            counts[key] = c
            durations[key] = d
        recency = np.nan
        past = s_fac[s_fac["siren_ts_end"] <= start]
        if not past.empty:
            recency = (start - past["siren_ts_end"].max()).total_seconds() / 60.0
        overlap = (
            (s_fac["siren_ts_start"] <= end) & (s_fac["siren_ts_end"] >= start)
        )
        overlap_sirens = s_fac[overlap]
        siren_during_case = int(not overlap_sirens.empty)
        siren_real_during_case = int(
            not overlap_sirens[overlap_sirens["classified_real"] == 1].empty
        )
        proximity_min = (
            overlap_sirens["proximity_km"].min() if siren_during_case else np.nan
        )
        feat_rows.append(
            {
                "case_id": op.case_id,
                "siren_count_6h": counts["6h"],
                "siren_count_24h": counts["24h"],
                "siren_dur_min_6h": durations["6h"],
                "siren_dur_min_24h": durations["24h"],
                "siren_recency_min": recency,
                "siren_during_case": siren_during_case,
                "siren_real_during_case": siren_real_during_case,
                "proximity_min_km_during_case": proximity_min,
            }
        )

    feat = pd.DataFrame(feat_rows)
    # exposure index
    dur_z = _zscore(feat["siren_dur_min_24h"])
    count_z = _zscore(feat["siren_count_24h"])
    proximity_term = 1 - np.minimum(feat["proximity_min_km_during_case"].fillna(20) / 20, 1)
    feat["exposure_index"] = (
        0.35 * dur_z + 0.25 * count_z + 0.25 * feat["siren_during_case"] + 0.15 * proximity_term
    ).round(3)
    return feat


def _zscore(s: pd.Series) -> pd.Series:
    mu = s.mean()
    sigma = s.std(ddof=0)
    if sigma == 0:
        return pd.Series(0, index=s.index)
    return (s - mu) / sigma
