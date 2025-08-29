"""Feature engineering orchestration."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
import yaml

from .cleaning import clean_operations, clean_siren_events
from .exposure import compute_exposure
from .ingest import load_csvs


def build_features(data_dir: Path, config_path: Path) -> pd.DataFrame:
    """Load raw CSVs, clean them and compute features."""
    cfg = yaml.safe_load(open(config_path))
    data = load_csvs(data_dir)
    ops = clean_operations(data["operations.csv"])
    sirens = clean_siren_events(data["siren_events.csv"])
    exposure = compute_exposure(ops, sirens)
    df = ops.merge(exposure, on="case_id")
    return df
