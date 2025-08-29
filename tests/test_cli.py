from pathlib import Path

from typer.testing import CliRunner

from stress_surgery.cli import app
from stress_surgery.data.ingest import make_synth_data


def test_cli_pipeline(tmp_path: Path):
    runner = CliRunner()
    data_dir = tmp_path / "raw"
    make_synth_data(data_dir)

    result = runner.invoke(app, ["validate", "--data-dir", str(data_dir)])
    assert result.exit_code == 0

    features_path = tmp_path / "features.parquet"
    result = runner.invoke(
        app,
        [
            "build-features",
            "--data-dir",
            str(data_dir),
            "--out",
            str(features_path),
            "--config",
            "config/config.yaml",
        ],
    )
    assert result.exit_code == 0
    assert features_path.exists()

    result = runner.invoke(
        app,
        ["train", "--features", str(features_path), "--model", "baseline"],
    )
    assert result.exit_code == 0
