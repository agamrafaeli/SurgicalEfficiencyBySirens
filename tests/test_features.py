from pathlib import Path

import pandas as pd

from stress_surgery.data.features import build_features
from stress_surgery.data.ingest import make_synth_data


def test_exposure_features(tmp_path: Path):
    data_dir = tmp_path / "raw"
    make_synth_data(data_dir)
    cfg = Path("config/config.yaml")
    df = build_features(data_dir, cfg)
    case1 = df.set_index("case_id").loc["c1"]
    case2 = df.set_index("case_id").loc["c2"]
    assert case1.siren_during_case == 1
    assert case2.siren_during_case == 0
    assert round(case2.siren_recency_min, 1) == 80.0
