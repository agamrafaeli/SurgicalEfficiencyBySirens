import pytest
import pandas as pd
import pandera as pa

from stress_surgery.data import schema


def test_operations_schema_valid():
    df = pd.DataFrame(
        {
            "case_id": ["c1"],
            "patient_id_hash": ["p"],
            "facility_id": ["f"],
            "start_ts": ["2024-01-01"],
            "end_ts": ["2024-01-01"],
            "urgency": ["elective"],
            "expected_duration_min": [60],
            "complication_intraop": [0],
            "complication_short_term": [0],
            "complication_long_term": [0],
        }
    )
    schema.operations_schema.validate(df)


def test_operations_schema_invalid():
    df = pd.DataFrame({"case_id": [1]})
    with pytest.raises(pa.errors.SchemaError):
        schema.operations_schema.validate(df)


def test_operations_schema_without_long_term_is_ok():
    df = pd.DataFrame(
        {
            "case_id": ["c1"],
            "patient_id_hash": ["p"],
            "facility_id": ["f"],
            "start_ts": ["2024-01-01"],
            "end_ts": ["2024-01-01"],
            "urgency": ["elective"],
            "expected_duration_min": [60],
            "complication_intraop": [0],
            "complication_short_term": [0],
            # intentionally omit complication_long_term (optional)
        }
    )
    schema.operations_schema.validate(df)
