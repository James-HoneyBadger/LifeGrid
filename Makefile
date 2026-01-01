# Makefile for LifeGrid project tasks

.PHONY: help install test lint format clean build docs release

help:
	@echo "LifeGrid Makefile Commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make install-dev - Install development dependencies"
	@echo "  make test        - Run test suite"
	@echo "  make coverage    - Run tests with coverage"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code with black and isort"
	@echo "  make typecheck   - Run mypy type checker"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make build       - Build distribution packages"
	@echo "  make docs        - Build Sphinx documentation"
	@echo "  make docs-serve  - Build and serve documentation locally"
	@echo "  make release     - Build release packages"
	@echo "  make executable  - Build standalone executable"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev,docs,export]"

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	pylint src/ || true

format:
	black src/ tests/ examples/
	isort src/ tests/ examples/

typecheck:
	mypy src/ --ignore-missing-imports

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build
	twine check dist/*

docs:
	cd docs && make html
	@echo "Documentation built in docs/_build/html/index.html"

docs-serve: docs
	cd docs/_build/html && python -m http.server 8000

release: clean test
	python -m build
	twine check dist/*
	@echo "Release packages ready in dist/"
	@echo "To upload: twine upload dist/*"

executable:
	pyinstaller lifegrid.spec
	@echo "Executable built in dist/"

run:
	python src/main.py

examples:
	@echo "Running example scripts..."
	python examples/scripts/basic_simulator.py
	python examples/scripts/pattern_explorer.py
