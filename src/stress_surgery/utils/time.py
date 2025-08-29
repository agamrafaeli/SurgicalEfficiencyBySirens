"""Time utilities for timezone aware operations."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

import pandas as pd

TZ = timezone.utc


def parse_ts(ts: str) -> datetime:
    """Parse ISO8601 string to timezone-aware datetime."""
    dt = pd.to_datetime(ts)
    if dt.tzinfo is None:
        dt = dt.tz_localize(TZ)
    return dt.to_pydatetime()


def overlap_minutes(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> float:
    """Return overlap in minutes between two intervals."""
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    delta = (earliest_end - latest_start).total_seconds()
    return max(delta, 0) / 60.0


def minutes_since(ts: datetime, ref: datetime) -> float:
    """Minutes between ts and reference (ts - ref)."""
    return (ts - ref).total_seconds() / 60.0
