.PHONY: all extract transform load clean init

all: extract transform load

extract:
	uv run python -m etl.extract

transform:
	uv run python -m etl.transform

load:
	uv run python -m etl.load

inspect:
	uv run python scripts/inspect_db.py

clean:
	rm -rf data/processed/*
	rm -rf data/interim/*
	rm -rf data/raw/*
