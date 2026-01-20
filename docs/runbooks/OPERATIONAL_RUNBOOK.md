# Operational Runbook - COCUS MVP

## 🛠️ Operations & Troubleshooting

This runbook provides the standard operating procedures (SOPs) for maintaining, deploying, and troubleshooting the COCUS MVP system.

## 🚀 Deployment Procedures

### 1. Local Development Setup
```bash
# Clone and setup environment
chmod +x setup.sh
./setup.sh

# Start the API
./run.sh
```

### 2. Docker Deployment
```bash
# Build and start services
docker-compose up --build -d

# Verify logs
docker-compose logs -f api
```

### 3. Google Cloud (Cloud Run)
```bash
# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/[PROJECT_ID]/cocus-mvp .

# Deploy to Cloud Run
gcloud run deploy cocus-mvp --image gcr.io/[PROJECT_ID]/cocus-mvp --platform managed
```

## 📋 Standard Operating Procedures (SOP)

### Data Ingestion & Refresh
When new data arrives:
1. Place new `.ndjson` files in `data/raw/`.
2. Run `python3 main.py` to trigger the full pipeline (Validation → Masking → Indexing).
3. Verify the acceptance rate in `reports/data_quality_report.md`.

### Model Retraining
If drift is detected:
1. Execute `python3 scripts/train_ml_model_real.py`.
2. Verify the new ONNX model in the `models/` directory.

## 🔍 Troubleshooting

### 1. API Fails to Start
- **Symptom**: `uvicorn` error on port 8000.
- **Solution**: Run `pkill -f uvicorn` and restart `./run.sh`. Check `.env` for missing variables.

### 2. Low Acceptance Rate (< 30%)
- **Symptom**: Too many rejected records in the data quality report.
- **Solution**: Check `src/models/order.py` validators. The raw data schema may have changed (e.g., date format or currency symbols). Update the Pydantic models to satisfy the new schema.

### 3. RAG Agent Hallucinations
- **Symptom**: Agent provides Order IDs that don't exist in the data.
- **Solution**: Check the retrieval tool in `scripts/run_business_questions.py`. Ensure the vector store is indexed with the correct masked data.

### 4. Docker Build Failures
- **Symptom**: `pip install` errors or base image not found.
- **Solution**: Verify the Docker registry credentials. Ensure `requirements.txt` is updated with compatible versions for the Python 3.11-alpine base image.

## 🆘 Emergency Contacts
- **ML Engineering**: [Your Name/Team]
- **Privacy Officer**: [Your Compliance Team]
- **Infrastructure**: [DevOps Lead]
