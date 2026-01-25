# COCUS MVP - Enterprise RAG System

**Production-ready ML + RAG system with GDPR compliance**

[![CI - Continuous Integration](https://github.com/H-Daoud/Cocus_Enterprise_MVP_ML_LLM_RAG_System/actions/workflows/ci.yml/badge.svg)](https://github.com/H-Daoud/Cocus_Enterprise_MVP_ML_LLM_RAG_System/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![GCP](https://img.shields.io/badge/GCP-ready-4285F4.svg)](https://cloud.google.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Overview

Complete end-to-end ML and RAG system featuring:
- ✅ **Data Validation** with Pydantic
- ✅ **GDPR Compliance** (EU AI Act ready)
- ✅ **ML Anomaly Detection** (ONNX export)
- ✅ **RAG System** with Hybrid Search
- ✅ **Production Deployment** (GCP & On-Premise)

---

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Environment**
```bash
cp .env.template .env
# Edit .env with your API keys
```

### **3. Run Complete Pipeline**
```bash
python3 main.py
```

### **4. Start API Server**
```bash
./scripts/run.sh
# Access: http://localhost:8000/frontend/chat-ui.html
```

---

## 📦 Deployment Options

### **☁️ Google Cloud Platform**
```bash
# Deploy to Cloud Run (recommended)
gcloud run deploy mvp-rag --source .
```

### **🐳 Docker**
```bash
# Using Docker Compose
docker-compose up -d
```

### **🏢 On-Premise**
```bash
# Systemd service or bare metal
# See docs/DEPLOYMENT_GUIDE.md
```

**📖 Full deployment guide**: [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md)

---

## 📁 Project Structure

```text
COCUS-MVP/
├── main.py                    # 🚀 Master orchestrator & Entry point
├── README.md                  # 📖 Essential project overview
│
├── scripts/                   # ⚡ Execution & Setup scripts
│   ├── run.sh                 # Start the FastAPI server
│   ├── setup.sh               # One-click environment setup
│   ├── reindex.sh             # Rebuild the RAG vector store
│   └── utils/                 # Utility scripts (testing, build)
│
├── src/                       # 🐍 Core Source Code
│   ├── api/                   # FastAPI backend (Routes, middleware)
│   ├── rag/                   # RAG Engine (Manager, retrieval)
│   ├── ml/                    # ML Logic (Training, anomaly detection)
│   ├── models/                # Pydantic data schemas
│   └── privacy/               # GDPR Masking & PII protection
│
├── docker/                    # 🐳 Containerization & Cloud
│   ├── docker-compose.yml     # Local orchestration
│   └── Dockerfile             # Production API image
│
├── frontend/                  # 🌐 User Interface
│   └── chat-ui.html           # Branded RAG Chat interface
│
├── docs/                      # 📚 Knowledge Base
│   ├── CHALLENGE_QA.md        # Consolidated Q&A
│   ├── QUICK_START.md         # 2-minute starter guide
│   └── internal_summaries/    # Technical deep-dives
│
├── data/                      # 💾 Data Layer
│   ├── raw/                   # Input datasets
│   ├── processed/             # Masked & validated data
│   └── vectorstore/           # ChromaDB index
│
└── models/                    # ⚙️ Model Storage (ONNX/PKL)
```

---

## 🎓 Key Features

### **Part 1: Data Validation & ML**
- **Pydantic Models**: Type-safe data validation
- **Data Quality**: 5 comprehensive analyses
- **ML Training**: Isolation Forest (unsupervised)
- **ONNX Export**: Production-ready format

### **Part 2: LLM-RAG System**
- **Hybrid Search**: Vector + Exact matching
- **Pydantic-AI Agent**: Structured outputs
- **Business Questions**: 3 core analyses
- **Audit Trail**: `used_order_ids` tracking

### **Enterprise Features**
- **GDPR Compliant**: Data masking, privacy by design
- **EU AI Act**: Transparency, record-keeping
- **Production Ready**: Docker, GCP, monitoring
- **Professional UI**: Branded chat interface

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Data Acceptance Rate** | 42% |
| **ML Anomaly Detection** | 9.5% |
| **Model Size (ONNX)** | 371 KB |
| **Docker Image** | ~400 MB |
| **Query Latency** | <100ms |
| **Training Time** | ~2 seconds |

---

## 🛡️ Compliance

- ✅ **GDPR Article 5**: Data minimization
- ✅ **GDPR Article 25**: Privacy by design
- ✅ **GDPR Article 13**: Transparency
- ✅ **EU AI Act Article 13**: Record-keeping

**All PII is masked before ML training and RAG indexing.**

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [`DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) | GCP & On-Premise deployment |
| [`COMPLETE_REQUIREMENTS_QA.md`](docs/COMPLETE_REQUIREMENTS_QA.md) | 25 Q&A for PM review |
| [`TEST_RESULTS.md`](docs/internal_summaries/TEST_RESULTS.md) | System test validation |
| [`PROJECT_STRUCTURE.md`](docs/internal_summaries/PROJECT_STRUCTURE.md) | File organization |

**📖 Full documentation index**: [`docs/README.md`](docs/README.md)

---

## 🔧 Development

### **Run Individual Components:**
```bash
# Data quality analysis
python3 scripts/data_quality_analysis.py

# ML training
python3 scripts/train_ml_model_real.py

# GDPR data processing
python3 scripts/process_data_gdpr.py
```

### **Run Tests:**
```bash
# All tests documented in docs/internal_summaries/TEST_RESULTS.md
python3 -m pytest tests/
```

---

## 🌐 API Endpoints

```
GET  /health          # Health check
GET  /metrics         # Prometheus metrics
POST /query           # RAG query
GET  /chat-ui.html    # Web interface
```

---

## 🎯 Use Cases

1. **Order Anomaly Detection**: Flag suspicious orders
2. **Business Intelligence**: Answer complex queries
3. **Data Quality**: Automated validation
4. **Compliance**: GDPR-ready data processing

---

## 🚢 Production Deployment

### **Recommended: Google Cloud Run**
```bash
# One-command deployment
gcloud run deploy mvp-rag \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
```

### **Alternative: Docker Compose**
```bash
# For on-premise or local deployment
docker-compose up -d
```

**See [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) for complete instructions.**

---

## 📈 Scaling

- **Cloud Run**: Auto-scales 0→N instances
- **GKE**: Kubernetes orchestration
- **On-Premise**: Systemd + load balancer

---

## 🔒 Security

- **API Keys**: Environment variables only
- **Secrets**: GCP Secret Manager integration
- **HTTPS**: Automatic (Cloud Run) or Let's Encrypt
- **Network**: Firewall rules, VPC

---

## 🤝 Support

- **Issues**: Check `TEST_RESULTS.md`
- **Deployment**: See `docs/DEPLOYMENT_GUIDE.md`
- **Questions**: Review `docs/COMPLETE_REQUIREMENTS_QA.md`

---

## ✅ Requirements Met

### **Part 1: Data Validation**
- [x] Pydantic models with business rules
- [x] Data quality analysis (5 questions)
- [x] ML model training (Isolation Forest)
- [x] ONNX export for production

### **Part 2: LLM-RAG**
- [x] RAG system with validated data
- [x] Hybrid Search (Vector + Exact)
- [x] Pydantic-AI agent
- [x] 3 business questions answered

### **Production Ready**
- [x] GDPR & EU AI Act compliance
- [x] Docker deployment
- [x] GCP Cloud Run ready
- [x] On-premise deployment
- [x] Complete documentation

---

## 📄 License

MIT License - See LICENSE file for details

---

**🚀 Production-ready ML + RAG system for enterprise deployment**
