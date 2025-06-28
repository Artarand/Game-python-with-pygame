.PHONY: all install lint run

help:
	@echo "Make sure you installed following tools:"
	@echo "- uv"
	@echo "Commands:"
	@echo " * lint: run linters formatters (ruff & mypy)"
	@echo " * all: run install, lint/format, and run game"
	@echo ""
	@echo "Requirement management"
	@echo ""
	@echo "* install: use uv and pyproject.toml to install all dependancies in virtualenv"
	@echo "* sync: sync the project's dependencies with the environment."

install:	
	uv venv --python 3.12
	# https://docs.astral.sh/uv/concepts/cache/#dependency-caching
	uv sync --refresh
	uv pip install -r pyproject.toml

sync:
	uv sync

lint:
	uvx ruff check --fix .
	uvx ruff format
	uvx ruff check --extend-select=I --fix

run:
	uv run shifumi

all: install sync lint run

clean:
	uv cache clean
	rm -rf .venv
	rm -rf .*_cache
	rm -rf htmlcov
	rm -rf wheels
	rm -rf junit-report.xml
	rm -rf .coverage