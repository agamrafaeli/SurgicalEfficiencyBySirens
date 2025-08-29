"""Exploratory data analysis utilities."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ..utils.plotting import savefig


def run_eda(df: pd.DataFrame, out_dir: Path) -> None:
    """Create simple exposure histogram."""
    fig, ax = plt.subplots()
    df["exposure_index"].hist(ax=ax)
    ax.set_title("Exposure index distribution")
    savefig(fig, out_dir / "exposure_hist.png")
