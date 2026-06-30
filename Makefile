.PHONY: *

default: tests

tests:
	uv run pytest

ty:
	uv run ty check

ruff:
	uv run ruff check

upload:
	rm -rf dist/* && uv build . && uv publish dist/* --verbose
