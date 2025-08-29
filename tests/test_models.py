from pathlib import Path

from stress_surgery.data.features import build_features
from stress_surgery.data.ingest import make_synth_data
from stress_surgery.models import baseline_logit


def test_baseline_logit_sign(tmp_path: Path):
    data_dir = tmp_path / "raw"
    make_synth_data(data_dir)
    df = build_features(data_dir, Path("config/config.yaml"))
    res = baseline_logit.fit(df)
    assert res["coef_exposure_index"] > 0
