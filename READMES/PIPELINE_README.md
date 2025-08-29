# Pipeline README

The pipeline is orchestrated via the `stress-surgery` CLI and `Makefile` targets. Main steps:
1. `validate` – run pandera schema checks on raw CSVs.
2. `build-features` – clean, merge and compute features.
3. `eda` – exploratory data analysis and figures.
4. `train` – fit statistical models.
5. `evaluate` – compute metrics and diagnostics.
6. `report` – render HTML reports.
