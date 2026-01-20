.PHONY: help install test lint format clean docker-build docker-up docker-down

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	cd frontend && npm install

test:  ## Run tests
	pytest tests/ -v --cov=src

test-unit:  ## Run unit tests only
	pytest tests/unit/ -v

test-integration:  ## Run integration tests only
	pytest tests/integration/ -v

lint:  ## Run linters
	flake8 src tests
	mypy src
	black --check src tests
	isort --check-only src tests

format:  ## Format code
	black src tests
	isort src tests

clean:  ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

docker-build:  ## Build Docker images
	docker-compose -f docker/docker-compose.yml build

docker-up:  ## Start Docker containers
	docker-compose -f docker/docker-compose.yml up -d

docker-down:  ## Stop Docker containers
	docker-compose -f docker/docker-compose.yml down

docker-logs:  ## View Docker logs
	docker-compose -f docker/docker-compose.yml logs -f

run-api:  ## Run API server locally
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:  ## Run frontend development server
	cd frontend && npm run dev

split-data:  ## Split dataset using Andrew Ng methodology
	python scripts/data/split_dataset.py --input data/raw/orders_sample.ndjson

validate-data:  ## Validate order data
	python scripts/data/validate_orders.py --input data/raw/orders_sample.ndjson
