# MLOps Lifecycle - COCUS MVP

## 🚀 Machine Learning Pipeline

The system utilizes a data-centric MLOps lifecycle, following best practices introduced by Andrew Ng. This ensures the model remains robust even when faced with low-quality or "dirty" data streams.

### 1. Data Collection & Versioning
- **Raw Data**: Stored in `data/raw/` (NDJSON format).
- **Versioning**: DVC (Data Version Control) is integrated in the `data/dvc/` directory to manage dataset iterations without bloating the Git repository.

### 2. Validation & Preprocessing (Privacy-First)
- **Validation**: Pydantic models in `src/models/` act as a gatekeeper.
- **Privacy**: GDPR masking happens before any training. This prevents PII leakage into model weights.
- **Handoff**: Cleaned, masked data is saved to `data/processed/orders_masked.ndjson`.

### 3. Model Training
- **Algorithm**: Isolation Forest (Unsupervised Anomaly Detection).
- **Execution**: Triggered via `scripts/train_ml_model_real.py`.
- **Environment**: Multi-stage training (Train/Dev/Test) demonstrated in `notebooks/Complete_ML_Pipeline_Andrew_Ng.ipynb`.

### 4. Continuous Integration & Deployment (CI/CD)
- **Format**: Models are exported to **ONNX** format for production consistency.
- **Automation**: GitHub Actions (configured in `.github/workflows/`) automate the testing and building of the containerized application.
- **Registry**: Docker images are pushed to a container registry for seamless deployment to GCP or on-premise servers.

## 📊 Monitoring & Maintenance

### Retraining Strategy
- **Trigger**: The system re-indexes and can re-train when the data acceptance rate drops significantly or when a new batch of orders is received.
- **Automation**: `main.py` serves as the orchestrator to ensure the pipeline remains up-to-date.

### Model Health Metrics
- **Anomaly Rate**: Monitored to detect concept drift. (Current: 9.5%).
- **Inference Latency**: Tracked via Prometheus to ensure real-time performance (<100ms).

## 🛠️ Tooling
- **Tracking**: MLflow (internal integration) for experiment management.
- **Export**: `skl2onnx` for Python to ONNX conversion.
- **Orchestration**: `Makefile` and `run.sh` for standardizing operations.
