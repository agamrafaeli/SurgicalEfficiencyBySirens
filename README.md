# Comparative Stress & Surgery Study

This repository estimates how acute air-raid siren stress affects surgical complication rates in Israeli hospitals. It treats siren occurrences as a natural experiment, compares exposed surgeries to suitable baselines, and adjusts for clinical complexity, staffing, fatigue, and workflow disruption. The codebase is fully CLI-driven, validated, and reproducible. The current pipeline models separate outcomes (intraoperative and short-term complications by default; long-term complications when available) and intentionally avoids a single composite “success” metric.


## What’s inside

src/stress_surgery: data validation, feature engineering, models (logit/GEE, DiD, Cox survival, propensity weighting), EDA, sensitivity, and HTML reporting.

* `data/`: raw inputs (CSV), intermediate, and processed feature tables.
* `reports/`: figures and templated HTML study reports.
* `config/config.yaml`: analysis settings (windows, matching, seeds).
* `docs/`: data dictionary and methodology notes.
* `READMES/`: focused guides for data, pipeline, models, and reports.

## Quick start

* `make install` → set up environment.

Place CSVs in `data/raw/` (see `READMES/DATA_README.md`).

* `make validate` → schema checks.
* `make build` → feature engineering.
* `make eda` → exploratory figures.
* `make train` → fit models (e.g., GEE).
* `make report` → produce `reports/html/study_report.html`.

Outputs include exposure metrics (count/duration/recency), disruption scores, team familiarity, fatigue indicators, and adjusted effect estimates with robust errors and sensitivity analyses for each complication outcome.
