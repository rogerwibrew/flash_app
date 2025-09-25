install: ## Install runtime dependencies
	pip install -e .

dev: ## Install runtime + dev dependencies
	pip install -e ".[dev]"

test: ## Run pytest with verbose output
	pytest -v

coverage: ## Run pytest with coverage (terminal report)
	pytest --cov=src --cov-report=term-missing

coverage-html: ## Run pytest with coverage (HTML report)
	pytest --cov=src --cov-report=html

clean: ## Clean up cache, build files, coverage, and DB
	rm -rf .pytest_cache .coverage coverage.xml htmlcov dist build *.egg-info flash.db
	find . -type d -name "__pycache__" -exec rm -rf {} +

run:
	flask --app flash.app run --debug

help: ## Show available make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

