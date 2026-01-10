
# Makefile for DevTools Helper
.PHONY: help install install-dev test lint format build clean publish-test publish

help:
	@echo "Available commands:"
	@echo "  install      - Install package in current environment"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting (flake8, mypy)"
	@echo "  format       - Format code (black, isort)"
	@echo "  build        - Build package distributions"
	@echo "  clean        - Clean build artifacts"
	@echo "  publish-test - Publish to TestPyPI"
	@echo "  publish      - Publish to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,test,docs]"

test:
	pytest tests/ -v --cov=devtools_helper --cov-report=term-missing

lint:
	flake8 devtools_helper tests --max-line-length=88
	mypy devtools_helper
	black --check devtools_helper tests

format:
	black devtools_helper tests
	isort devtools_helper tests

build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*
