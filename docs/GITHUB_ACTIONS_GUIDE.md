# GitHub Actions CI/CD Guide

## Overview
This guide explains the automated CI/CD pipelines configured for your MVP.

---

## Available Workflows

### 1. **Automated Testing** (`.github/workflows/test.yml`)
**Triggers:** Every push to `main` or pull request

**What it does:**
- Runs data validation tests
- Executes data quality analysis
- Validates Pydantic models
- Checks code quality

**How to use:**
```bash
# Just push your code - tests run automatically
git add .
git commit -m "Add new feature"
git push origin main
```

---

### 2. **ML Model Training** (`.github/workflows/train_model.yml`)
**Triggers:** 
- Manual trigger (workflow_dispatch)
- When new data is added to `data/raw/`

**What it does:**
- Detects new data files
- Trains anomaly detection model
- Exports to ONNX format
- Saves model artifacts
- Creates GitHub Release with model

**How to use:**
```bash
# Option 1: Automatic (when you add new data)
git add data/raw/new_orders.ndjson
git commit -m "Add new order data"
git push

# Option 2: Manual trigger
# Go to GitHub → Actions → "Train ML Model" → Run workflow
```

---

### 3. **Docker Build & Deploy** (`.github/workflows/deploy.yml`)
**Triggers:**
- Push to `main` branch
- New release tag (e.g., `v1.0.0`)

**What it does:**
- Builds optimized Docker image
- Pushes to Google Container Registry
- Deploys to Google Cloud Run
- Updates production environment

**How to use:**
```bash
# Deploy to production
git tag v1.0.0
git push origin v1.0.0

# Or just push to main for staging
git push origin main
```

---

## Setup Instructions

### **Step 1: Configure GitHub Secrets**

Go to: **GitHub Repo → Settings → Secrets and variables → Actions**

Add these secrets:

| Secret Name | Value | Purpose |
|-------------|-------|---------|
| `OPENAI_API_KEY` | Your HuggingFace token | LLM API access |
| `GCP_PROJECT_ID` | Your Google Cloud project ID | Deployment target |
| `GCP_SA_KEY` | Service account JSON key | Authentication |

**How to get GCP Service Account Key:**
```bash
# 1. Create service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

# 2. Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

# 3. Create key
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 4. Copy the contents of key.json to GitHub Secret GCP_SA_KEY
```

---

### **Step 2: Enable GitHub Actions**

1. Go to your repo → **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"
3. Workflows will now run automatically

---

## Workflow Examples

### **Example 1: Add New Data & Auto-Train**

```bash
# 1. Add new order data
cp ~/Downloads/new_orders.ndjson data/raw/

# 2. Commit and push
git add data/raw/new_orders.ndjson
git commit -m "Add Q1 2026 orders"
git push

# 3. GitHub Actions will:
#    - Run tests
#    - Detect new data
#    - Train ML model
#    - Create release with model artifacts
```

---

### **Example 2: Deploy New Version**

```bash
# 1. Make your changes
git add src/rag/manager.py
git commit -m "Improve hybrid search accuracy"

# 2. Create release
git tag v1.1.0
git push origin v1.1.0

# 3. GitHub Actions will:
#    - Build Docker image
#    - Push to GCR
#    - Deploy to Cloud Run
#    - Update production URL
```

---

### **Example 3: Manual Model Training**

1. Go to **GitHub → Actions**
2. Select **"Train ML Model"** workflow
3. Click **"Run workflow"**
4. Select branch (usually `main`)
5. Click **"Run workflow"** button

The trained model will be available in **Releases** section.

---

## Monitoring & Logs

### **View Workflow Status**
- Go to: **GitHub → Actions**
- Click on any workflow run
- Expand steps to see detailed logs

### **Download Artifacts**
- Go to: **GitHub → Actions → [Workflow Run]**
- Scroll to **Artifacts** section
- Download:
  - `ml-model` (ONNX + metadata)
  - `test-reports` (coverage, quality analysis)
  - `docker-image-digest` (deployment info)

---

## Troubleshooting

### **Workflow Fails: "Authentication Error"**
**Fix:** Check that `GCP_SA_KEY` secret is correctly set

### **Model Training Fails: "No data found"**
**Fix:** Ensure `data/raw/*.ndjson` files exist in the repo

### **Docker Build Fails: "Out of memory"**
**Fix:** GitHub Actions has 7GB RAM limit. Use the slim Dockerfile:
```yaml
# In .github/workflows/deploy.yml
- name: Build Docker image
  run: docker build -f Dockerfile.slim -t app .
```

---

## Best Practices

### **1. Branch Protection**
Enable in: **Settings → Branches → Add rule**
- Require status checks to pass before merging
- Require pull request reviews

### **2. Scheduled Training**
Add to `.github/workflows/train_model.yml`:
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
```

### **3. Notifications**
Get Slack/Email alerts when workflows fail:
```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Summary

**What's Automated:**
✅ Testing on every push  
✅ ML training when new data arrives  
✅ Docker builds and deployments  
✅ Model versioning and releases  

**What You Do:**
1. Push code changes
2. Add new data files
3. Create release tags

**GitHub Actions handles the rest!** 🚀
