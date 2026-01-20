# Docker Deployment Guide

## Quick Start

### 1. Build the Docker Image
```bash
./docker-build.sh
```
This will show you the final image size (~2-3 GB).

### 2. Test Locally
```bash
# Make sure your .env file exists with your API keys
docker-compose -f docker-compose.simple.yml up
```

Access the UI at: `http://localhost:8000/chat-ui.html`

---

## Security: API Keys

**IMPORTANT**: Your API keys are **NEVER** stored in the Docker image.

### How It Works:
1. **Local Testing**: Keys are read from your `.env` file (which is in `.gitignore`)
2. **Cloud Deployment**: Keys are passed as environment variables or stored in Google Secret Manager

### Example .env file:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=hf_your_huggingface_token_here
OPENAI_API_BASE=https://router.huggingface.co/v1
OPENAI_MODEL=meta-llama/Llama-3.2-3B-Instruct
```

---

## Deploy to Google Cloud Run

### Prerequisites:
```bash
# Install Google Cloud CLI
brew install google-cloud-sdk

# Login
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### Deploy:
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mvp-rag-system

# Deploy to Cloud Run (with secrets)
gcloud run deploy mvp-rag-system \
  --image gcr.io/YOUR_PROJECT_ID/mvp-rag-system \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LLM_PROVIDER=openai \
  --set-env-vars OPENAI_API_BASE=https://router.huggingface.co/v1 \
  --set-env-vars OPENAI_MODEL=meta-llama/Llama-3.2-3B-Instruct \
  --update-secrets OPENAI_API_KEY=huggingface-api-key:latest
```

**Note**: First create the secret:
```bash
echo -n "your_hf_token" | gcloud secrets create huggingface-api-key --data-file=-
```

---

## Image Size Breakdown

| Component | Size |
|-----------|------|
| Base Python 3.11 | ~900 MB |
| Dependencies (FastAPI, LangChain, etc.) | ~800 MB |
| HuggingFace Embeddings | ~500 MB |
| Your Code | ~10 MB |
| **Total** | **~2.2 GB** |

**Note**: Vector store data is mounted as a volume, not included in the image.

---

## Cost Estimate (Google Cloud Run)

For 10-50 employees with moderate usage:
- **Cloud Run**: $5-15/month (pay per request)
- **Cloud Storage** (for data): $1-3/month
- **Total**: ~$10-20/month

---

## Next Steps

1. Test locally: `docker-compose -f docker-compose.simple.yml up`
2. Verify the system works
3. Deploy to Google Cloud Run
4. Share the URL with your logistics team
