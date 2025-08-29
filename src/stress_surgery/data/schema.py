"""Pandera schemas for input CSV files."""
from __future__ import annotations

import pandera as pa
from pandera import Check, Column, DataFrameSchema


operations_schema = DataFrameSchema(
    {
        "case_id": Column(pa.String, unique=True),
        "patient_id_hash": Column(pa.String),
        "facility_id": Column(pa.String),
        "start_ts": Column(pa.DateTime),
        "end_ts": Column(pa.DateTime),
        "urgency": Column(pa.Category, Check.isin(["elective", "urgent", "emergent"])),
        "expected_duration_min": Column(pa.Int, Check.ge(0)),
        "success_primary": Column(pa.Int, Check.isin([0, 1])),
    },
    strict=False,
)

siren_events_schema = DataFrameSchema(
    {
        "facility_id": Column(pa.String),
        "siren_ts_start": Column(pa.DateTime),
        "siren_ts_end": Column(pa.DateTime),
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
