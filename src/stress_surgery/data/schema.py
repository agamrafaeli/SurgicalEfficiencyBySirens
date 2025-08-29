"""Pandera schemas for input CSV files."""
from __future__ import annotations

import pandera as pa
from pandera import Check, Column, DataFrameSchema


operations_schema = DataFrameSchema(
    {
        "case_id": Column(pa.String, unique=True),
        "patient_id_hash": Column(pa.String),
        "facility_id": Column(pa.String),
        "start_ts": Column(pa.DateTime, coerce=True),
        "end_ts": Column(pa.DateTime, coerce=True),
        "urgency": Column(pa.Category, Check.isin(["elective", "urgent", "emergent"]), coerce=True),
        "expected_duration_min": Column(pa.Int, Check.ge(0)),
        # Complication indicators (0/1)
        "complication_intraop": Column(pa.Int, Check.isin([0, 1])),
        "complication_short_term": Column(pa.Int, Check.isin([0, 1])),
        # Long-term complications are planned but often unavailable yet; make optional
        "complication_long_term": Column(pa.Int, Check.isin([0, 1]), required=False),
    },
    strict=False,
)

siren_events_schema = DataFrameSchema(
    {
        "facility_id": Column(pa.String),
        "siren_ts_start": Column(pa.DateTime, coerce=True),
        "siren_ts_end": Column(pa.DateTime, coerce=True),
        "proximity_km": Column(pa.Float, Check.ge(0)),
        "classified_real": Column(pa.Int, Check.isin([0, 1])),
    },
    strict=False,
)

SCHEMAS = {
    "operations": operations_schema,
    "siren_events": siren_events_schema,
}


def get_schema(name: str) -> DataFrameSchema:
    """Return schema by name."""
    return SCHEMAS[name]
