.PHONY: *

default: tests

repl:
	uv run python

tests:
	uv run pytest -v

ty:
	uv run ty check

ruff:
	uv run ruff check

upload:
	rm -rf dist/* && uv build . && uv publish dist/* --verbose
