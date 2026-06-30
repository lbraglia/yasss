.PHONY: *

default: tests

repl:
	uv run python

tests:
	uv run pytest -v

lint:
	uv run ruff check

format:
	uv run ruff format

upload:
	rm -rf dist/* && uv build . && uv publish dist/* --verbose
