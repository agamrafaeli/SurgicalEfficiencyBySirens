"""Data ingestion utilities and synthetic data generator."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .schema import get_schema
from ..utils import io
from ..utils.time import parse_ts


RAW_FILES = [
    "operations.csv",
    "siren_events.csv",
]


def load_csvs(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load required CSVs from a directory."""
    data = {}
    for fname in RAW_FILES:
        path = data_dir / fname
        if path.exists():
            data[fname] = io.read_csv(path)
    return data


def make_synth_data(out_dir: Path) -> None:
    """Generate small synthetic dataset for tests and examples."""
    rng = np.random.default_rng(42)
    out_dir.mkdir(parents=True, exist_ok=True)

    ops = pd.DataFrame(
        {
            "case_id": ["c1", "c2"],
            "patient_id_hash": ["p1", "p2"],
            "facility_id": ["f1", "f1"],
            "start_ts": pd.to_datetime(["2024-01-01T08:00:00+00:00", "2024-01-01T10:00:00+00:00"]),
            "end_ts": pd.to_datetime(["2024-01-01T09:00:00+00:00", "2024-01-01T11:00:00+00:00"]),
            "urgency": ["elective", "urgent"],
            "expected_duration_min": [60, 60],
            "success_primary": [1, 0],
        }
    )
    ops.to_csv(out_dir / "operations.csv", index=False)

    sirens = pd.DataFrame(
        {
            "facility_id": ["f1"],
            "siren_ts_start": pd.to_datetime(["2024-01-01T08:30:00+00:00"]),
            "siren_ts_end": pd.to_datetime(["2024-01-01T08:40:00+00:00"]),
            "proximity_km": [0.0],
            "classified_real": [1],
        }
    )
    sirens.to_csv(out_dir / "siren_events.csv", index=False)
