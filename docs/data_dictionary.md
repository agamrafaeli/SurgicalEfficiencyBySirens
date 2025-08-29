# Data Dictionary

This document lists major variables used in the analysis. Timezone is `Asia/Jerusalem` for all timestamps.

## operations.csv
- `case_id`: Unique case identifier.
- `patient_id_hash`: De-identified patient hash.
- `facility_id`: Hospital facility identifier.
- `start_ts`, `end_ts`: ISO8601 timestamps for operation start and end.
- `urgency`: elective/urgent/emergent.
- `success_primary`: Composite success indicator.

## siren_events.csv
- `facility_id`: Facility affected by siren.
- `siren_ts_start`, `siren_ts_end`: Start and end times of siren window.
- `proximity_km`: Distance in km; 0 means at facility.
- `classified_real`: 1 if real siren, 0 otherwise.

Further details and derived features are documented in code comments.
