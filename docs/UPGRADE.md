# Upgrade Guide: Outcomes → Complications

This repository no longer supports a single “successful/unsuccessful” outcome field. Analyses target complication indicators separately:

- `complication_intraop`: 0/1 intraoperative complication
- `complication_short_term`: 0/1 short-term postoperative complication
- `complication_long_term` (optional): 0/1 long-term complication (often unavailable in current Israeli data)

## CSV changes

- `operations.csv` must include `complication_intraop` and `complication_short_term` columns. The `complication_long_term` column is optional.
- Any legacy columns like `success`, `successful`, `unsuccessful`, `outcome_success`, etc., should be removed or mapped to the appropriate complication indicators if you have a defensible definition.

The `stress-surgery validate` command will warn if legacy outcome columns are detected.

## Model usage

- Commands and APIs accept an `outcome` argument referring to one of the complication columns (e.g., `complication_intraop`).
- There is no composite outcome in the codebase. If you need one, construct it externally and save as a new column, then pass it as the `outcome`.

## Migration tips

- If you previously stored a single `success` flag, decide whether it reflected intraoperative or short-term complications and copy it accordingly. Avoid conflating multiple time horizons into one flag.
- If you cannot split the legacy flag, prefer dropping it and starting fresh with explicitly defined complication indicators.

