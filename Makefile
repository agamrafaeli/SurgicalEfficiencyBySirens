.PHONY: install format lint test validate build eda train report all

install:
pip install -r requirements.txt
pip install -e .

format:
black src tests
isort src tests

lint:
flake8 src tests

test:
pytest -q

validate:
stress-surgery validate --data-dir data/raw

build:
stress-surgery build-features --data-dir data/raw --out data/processed/features.parquet --config config/config.yaml

eda:
stress-surgery eda --features data/processed/features.parquet --out reports/figures

train:
stress-surgery train --features data/processed/features.parquet --model baseline

report:
stress-surgery report --features data/processed/features.parquet --model baseline --template src/stress_surgery/reporting/templates/report.html.j2 --out reports/html/study_report.html

all: install format lint test
