.PHONY: install dev test coverage clean

# Install runtime dependencies
install:
	pip install -e .

# Install with dev dependencies (pytest, pytest-cov, etc.)
dev:
	pip install -e ".[dev]"

# Run tests quickly
test:
	pytest -v

# Run tests with coverage report
coverage:
	pytest --cov=src --cov-report=term-missing

# Run tests with HTML coverage report
coverage-html:
	pytest --cov=src --cov-report=html

# Remove caches, build files, coverage reports, and local DB
clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov dist build *.egg-info flash.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
