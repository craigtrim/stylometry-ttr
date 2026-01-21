.PHONY: all install test lint format clean build publish

all: install lint test

install:
	poetry install

test:
	poetry run pytest -v

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

clean:
	rm -rf dist/ build/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	poetry build

publish: build
	poetry publish
