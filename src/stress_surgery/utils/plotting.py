"""Common plotting helpers."""
from pathlib import Path
import matplotlib.pyplot as plt


def savefig(fig: plt.Figure, path: Path) -> None:
    """Save a figure to disk ensuring directory exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
