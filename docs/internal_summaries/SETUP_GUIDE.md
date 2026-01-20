# 🚀 Complete Setup Guide - COCUS MVP ML/LLM RAG System

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Python Environment Setup](#step-1-python-environment-setup)
3. [Step 2: Environment Variables & API Keys](#step-2-environment-variables--api-keys)
4. [Step 3: Docker Setup](#step-3-docker-setup)
5. [Step 4: GitHub Actions Setup](#step-4-github-actions-setup)
6. [Step 5: Running the Application](#step-5-running-the-application)
7. [Step 6: Testing](#step-6-testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- ✅ Python 3.10 or higher
- ✅ Docker Desktop installed
- ✅ Git installed
- ✅ GitHub account (for GitHub Actions)
- ⚠️ OpenAI API key (optional, needed only for RAG functionality)

---

## Step 1: Python Environment Setup

### 1.1 Create Virtual Environment

```bash
cd /Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### 1.2 Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional, for testing/linting)
pip install -r requirements-dev.txt
```

**Expected output:** Installation of ~50+ packages including FastAPI, Pydantic, pandas, etc.

---

## Step 2: Environment Variables & API Keys

### 2.1 Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### 2.2 Configure API Keys

Edit `.env` file with your actual values:

```bash
# Open in your editor
nano .env
# OR
code .env  # If using VS Code
```

### 2.3 **API Keys Needed:**

#### **🔑 OpenAI API Key (for RAG functionality)**

**Do you need it?**
- ✅ **YES** - If you want to use the RAG (Retrieval-Augmented Generation) chat feature
- ❌ **NO** - If you only want to use data validation features

**How to get it:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key and add to `.env`:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

#### **Other API Keys (Optional for MVP):**

```bash
# Database (uses Docker defaults for local development)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cocus_mvp
REDIS_URL=redis://localhost:6379/0

# MLflow (uses Docker defaults)
MLFLOW_TRACKING_URI=http://localhost:5000

# AWS (only needed if using S3 for data storage)
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret

# Security (generate random strings for production)
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=dev-jwt-secret-change-in-production
```

### 2.4 Minimal Configuration for Quick Start

For a quick start, you only need:

```bash
# .env file (minimal)
OPENAI_API_KEY=sk-your-key-here  # Optional, only for RAG
DATABASE_URL=postgresql://postgres:postgres@db:5432/cocus_mvp
REDIS_URL=redis://redis:6379/0
MLFLOW_TRACKING_URI=http://mlflow:5000
```

---

## Step 3: Docker Setup

### 3.1 Install Docker Desktop

If not already installed:
- **macOS**: Download from https://www.docker.com/products/docker-desktop/
- **Windows**: Download from https://www.docker.com/products/docker-desktop/
- **Linux**: Follow https://docs.docker.com/engine/install/

### 3.2 Verify Docker Installation

```bash
docker --version
docker-compose --version
```

Expected output:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

### 3.3 Build Docker Images

```bash
# Build all Docker images
docker-compose -f docker/docker-compose.yml build

# This will build:
# - API service (FastAPI backend)
# - Frontend service (React app)
# - PostgreSQL database
# - Redis cache
# - MLflow tracking server
# - Prometheus monitoring
# - Grafana dashboards
```

**⏱️ This may take 5-10 minutes the first time.**

### 3.4 Start All Services

```bash
# Start all services in detached mode
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Check running containers
docker ps
```

### 3.5 Verify Services are Running

```bash
# Check service health
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","timestamp":"...","version":"1.0.0",...}
```

---

## Step 4: GitHub Actions Setup

### 4.1 Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Enterprise MVP structure"
```

### 4.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `COCUS-MVP_ML_LLM_RAG_System`)
3. **Don't** initialize with README (we already have one)

### 4.3 Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/COCUS-MVP_ML_LLM_RAG_System.git

# Push code
git branch -M main
git push -u origin main
```

### 4.4 Configure GitHub Secrets

For GitHub Actions to work, add these secrets:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these secrets:

| Secret Name | Value | Required For |
|------------|-------|--------------|
| `SNYK_TOKEN` | Your Snyk API token | Security scanning |
| `OPENAI_API_KEY` | Your OpenAI key | RAG functionality |
| `AWS_ACCESS_KEY_ID` | AWS key | DVC/S3 (optional) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret | DVC/S3 (optional) |
| `MLFLOW_TRACKING_URI` | MLflow server URL | ML pipeline |

**How to get Snyk token:**
1. Sign up at https://snyk.io/
2. Go to Account Settings → API Token
3. Copy the token

### 4.5 GitHub Actions Workflows

The following workflows are already configured in `.github/workflows/`:

- ✅ **CI** (`ci.yml`) - Runs on every push/PR
  - Code quality checks (flake8, black, mypy)
  - Unit and integration tests
  - Code coverage

- ✅ **Security Scan** (`security-scan.yml`) - Runs weekly
  - Dependency vulnerability scanning (Snyk)
  - Code security analysis (Bandit)
  - Container scanning (Trivy)

- ✅ **ML Pipeline** (`ml-pipeline.yml`) - Manual trigger
  - Dataset splitting
  - Model training
  - Model validation

- ✅ **Docker Build** (`docker-build.yml`) - Runs on main branch
  - Builds Docker images
  - Pushes to GitHub Container Registry

### 4.6 Trigger GitHub Actions

```bash
# Make a change and push
echo "# Test" >> README.md
git add README.md
git commit -m "Test GitHub Actions"
git push

# Go to GitHub → Actions tab to see workflows running
```

---

## Step 5: Running the Application

### Option A: Using Docker (Recommended)

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Access services:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
# - Frontend: http://localhost:3000
# - Grafana: http://localhost:3001 (admin/admin)
# - Prometheus: http://localhost:9090
# - MLflow: http://localhost:5000
```

### Option B: Running Locally (Development)

#### Terminal 1: API Server
```bash
source venv/bin/activate
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2: Frontend (if developing frontend)
```bash
cd frontend
npm install
npm run dev
```

### 5.1 Test the API

```bash
# Health check
curl http://localhost:8000/api/health

# API documentation
open http://localhost:8000/api/docs

# Test validation endpoint
curl -X POST "http://localhost:8000/api/validation/validate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/raw/orders_sample.ndjson"

# Test RAG endpoint (requires OpenAI API key)
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is data validation?", "max_results": 5}'
```

---

## Step 6: Testing

### 6.1 Run Unit Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### 6.2 Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Test a specific file
pytest tests/unit/test_models.py -v
```

### 6.3 Run Linters

```bash
# Format code
black src tests

# Check imports
isort src tests

# Lint code
flake8 src tests

# Type checking
mypy src
```

### 6.4 Use Makefile Commands

```bash
# Run all tests
make test

# Run linters
make lint

# Format code
make format

# Clean build artifacts
make clean
```

---

## Step 7: Data Processing

### 7.1 Split Dataset (Andrew Ng Methodology)

```bash
# Split the sample data
python scripts/data/split_dataset.py \
  --input data/raw/orders_sample.ndjson \
  --output-dir data/processed \
  --train-ratio 0.70 \
  --train-dev-ratio 0.10 \
  --dev-ratio 0.10 \
  --test-ratio 0.10

# Check the splits
ls -lh data/processed/
# Should see: train.ndjson, train_dev.ndjson, dev.ndjson, test.ndjson
```

### 7.2 Validate Data

```bash
# Validate order data
python -c "
from src.models.order import Order
import json

with open('data/raw/orders_sample.ndjson') as f:
    for line in f:
        try:
            data = json.loads(line)
            order = Order(**data)
            print(f'✅ Valid: {order.order_id}')
        except Exception as e:
            print(f'❌ Invalid: {str(e)[:50]}')
"
```

---

## Troubleshooting

### Issue 1: Docker containers won't start

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove volumes
docker-compose down -v

# Rebuild and start
docker-compose build --no-cache
docker-compose up -d
```

### Issue 2: Port already in use

**Solution:**
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
```

### Issue 3: Python dependencies installation fails

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies one by one to find the issue
pip install pydantic
pip install fastapi
# etc.
```

### Issue 4: OpenAI API key not working

**Check:**
```bash
# Verify .env file is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Issue 5: GitHub Actions failing

**Check:**
1. Secrets are correctly set in GitHub repository settings
2. Workflow files have correct syntax
3. View logs in GitHub Actions tab for specific errors

### Issue 6: Frontend not connecting to API

**Solution:**
```bash
# Check API is running
curl http://localhost:8000/api/health

# Check frontend proxy configuration in frontend/vite.config.ts
# Ensure proxy target is correct
```

---

## Quick Reference Commands

```bash
# Development
make install          # Install dependencies
make run-api          # Run API server
make run-frontend     # Run frontend
make test             # Run tests
make lint             # Run linters
make format           # Format code

# Docker
make docker-build     # Build images
make docker-up        # Start containers
make docker-down      # Stop containers
make docker-logs      # View logs

# Data
make split-data       # Split dataset
make validate-data    # Validate data

# Cleanup
make clean            # Clean build artifacts
docker system prune   # Clean Docker resources
```

---

## Next Steps

1. ✅ Complete this setup guide
2. ✅ Test the API endpoints
3. ✅ Run the test suite
4. ✅ Split the dataset
5. ⏭️ Implement RAG functionality
6. ⏭️ Build frontend components
7. ⏭️ Deploy to staging environment

---

## Support

- **Documentation**: See `../../README.md` for full documentation
- **Architecture**: See `./ENTERPRISE_TREE_STRUCTURE.txt`
- **Quick Reference**: See `./ENTERPRISE_QUICK_REFERENCE.txt`

---

**🎉 You're all set! The application is ready for development and testing.**
