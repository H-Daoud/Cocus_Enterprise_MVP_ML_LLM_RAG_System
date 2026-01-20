# 🚀 Deployment Guide - GCP & On-Premise

**Production deployment options for COCUS MVP**

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Google Cloud Platform (GCP)](#google-cloud-platform-gcp)
3. [On-Premise Deployment](#on-premise-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Health Checks & Monitoring](#health-checks--monitoring)

---

## 🎯 Quick Start

### **Prerequisites:**
- Python 3.11+
- Docker (optional)
- GCP account (for cloud deployment)

### **Install Dependencies:**
```bash
pip install -r requirements.txt
```

### **Run Locally:**
```bash
python3 main.py  # Complete pipeline
./run.sh         # Start API server
```

---

## ☁️ Google Cloud Platform (GCP)

### **Option 1: Cloud Run (Recommended)** ⭐

**Why Cloud Run?**
- ✅ Serverless (no infrastructure management)
- ✅ Auto-scaling (0 to N instances)
- ✅ Pay-per-use (cost-effective)
- ✅ HTTPS by default

#### **Step 1: Setup GCP Project**
```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### **Step 2: Deploy to Cloud Run**
```bash
# Deploy directly from source
gcloud run deploy mvp-rag \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
```

#### **Step 3: Access Your Service**
```bash
# Get the service URL
gcloud run services describe mvp-rag --region us-central1 --format 'value(status.url)'
```

**Expected Output:**
```
https://mvp-rag-xxxxx-uc.a.run.app
```

---

### **Option 2: Google Kubernetes Engine (GKE)**

**Why GKE?**
- ✅ Full Kubernetes control
- ✅ Multi-region deployment
- ✅ Advanced networking
- ✅ Enterprise features

#### **Step 1: Create GKE Cluster**
```bash
gcloud container clusters create mvp-cluster \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --region=us-central1
```

#### **Step 2: Deploy Application**
```bash
# Build and push Docker image
docker build -t gcr.io/$PROJECT_ID/mvp-rag:latest .
docker push gcr.io/$PROJECT_ID/mvp-rag:latest

# Deploy to GKE
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

#### **Step 3: Expose Service**
```bash
kubectl expose deployment mvp-rag --type=LoadBalancer --port=80 --target-port=8000
```

---

### **Option 3: Compute Engine (VM)**

**Why Compute Engine?**
- ✅ Full VM control
- ✅ Custom configurations
- ✅ Persistent storage
- ✅ SSH access

#### **Step 1: Create VM Instance**
```bash
gcloud compute instances create mvp-vm \
  --machine-type=n1-standard-2 \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --tags=http-server,https-server
```

#### **Step 2: SSH and Deploy**
```bash
# SSH into VM
gcloud compute ssh mvp-vm

# Install dependencies
sudo apt update
sudo apt install -y python3.11 python3-pip docker.io

# Clone and run
git clone <your-repo>
cd COCUS-MVP_ML_LLM_RAG_System
pip3 install -r requirements.txt
python3 main.py
```

---

## 🏢 On-Premise Deployment

### **Option 1: Docker Compose (Recommended)** ⭐

**Why Docker Compose?**
- ✅ Easy setup
- ✅ Isolated environment
- ✅ Reproducible
- ✅ Production-ready

#### **Step 1: Install Docker**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
docker --version
docker-compose --version
```

#### **Step 2: Configure Environment**
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
PORT=8000
EOF
```

#### **Step 3: Deploy**
```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### **Step 4: Access Application**
```
http://localhost:8000
http://localhost:8000/chat-ui.html
```

---

### **Option 2: Systemd Service (Linux)**

**Why Systemd?**
- ✅ Auto-start on boot
- ✅ Process management
- ✅ Logging integration
- ✅ Native Linux support

#### **Step 1: Create Service File**
```bash
sudo nano /etc/systemd/system/mvp-rag.service
```

```ini
[Unit]
Description=COCUS MVP RAG Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/COCUS-MVP_ML_LLM_RAG_System
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **Step 2: Enable and Start**
```bash
sudo systemctl daemon-reload
sudo systemctl enable mvp-rag
sudo systemctl start mvp-rag

# Check status
sudo systemctl status mvp-rag
```

---

### **Option 3: Bare Metal (Direct Installation)**

**Why Bare Metal?**
- ✅ Maximum performance
- ✅ No containerization overhead
- ✅ Direct hardware access
- ✅ Custom optimization

#### **Step 1: Install Python**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate
```

#### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **Step 3: Run Application**
```bash
# Complete pipeline
python3 main.py

# API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

---

## 🔧 Environment Configuration

### **Required Environment Variables:**

```bash
# API Configuration
OPENAI_API_KEY=sk-...           # Required
OPENAI_API_BASE=https://...     # Optional
OPENAI_MODEL=gpt-3.5-turbo      # Optional

# Application Settings
PORT=8000                        # Default: 8000
HOST=0.0.0.0                    # Default: 0.0.0.0
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR

# Database (if using external)
DATABASE_URL=postgresql://...   # Optional
REDIS_URL=redis://...           # Optional
```

### **GCP-Specific Variables:**

```bash
# Google Cloud
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GCP_SERVICE_ACCOUNT=...

# Cloud Storage (optional)
GCS_BUCKET=your-bucket-name
```

### **Security Variables:**

```bash
# Secrets (use Secret Manager in production)
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

---

## 🏥 Health Checks & Monitoring

### **Health Check Endpoint:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-20T08:00:00Z"
}
```

### **Monitoring Endpoints:**
```bash
# Metrics
curl http://localhost:8000/metrics

# Readiness
curl http://localhost:8000/ready

# Liveness
curl http://localhost:8000/alive
```

---

## 📊 Deployment Comparison

| Feature | Cloud Run | GKE | Compute Engine | On-Premise |
|---------|-----------|-----|----------------|------------|
| **Setup Time** | 5 min | 30 min | 15 min | 20 min |
| **Cost** | Low | Medium | Medium | Hardware only |
| **Scaling** | Auto | Manual/Auto | Manual | Manual |
| **Maintenance** | None | Medium | High | High |
| **Control** | Low | High | High | Full |
| **Best For** | MVP, Demo | Production | Custom needs | Enterprise |

---

## 🎯 Recommended Deployment

### **For MVP/Demo:**
```bash
# Cloud Run (easiest)
gcloud run deploy mvp-rag --source .
```

### **For Production:**
```bash
# GKE with auto-scaling
kubectl apply -f kubernetes/
```

### **For On-Premise:**
```bash
# Docker Compose
docker-compose up -d
```

---

## 🔒 Security Best Practices

### **1. API Keys:**
```bash
# Never commit API keys
# Use environment variables or secret managers

# GCP Secret Manager
gcloud secrets create openai-api-key --data-file=-
echo -n "your-api-key" | gcloud secrets create openai-api-key --data-file=-
```

### **2. Network Security:**
```bash
# GCP Firewall
gcloud compute firewall-rules create allow-http \
  --allow tcp:80,tcp:443 \
  --target-tags http-server
```

### **3. HTTPS:**
```bash
# Cloud Run (automatic HTTPS)
# For on-premise, use Let's Encrypt:
sudo certbot --nginx -d yourdomain.com
```

---

## 📈 Scaling Guidelines

### **Vertical Scaling (More Resources):**
```bash
# GCP Compute Engine
gcloud compute instances set-machine-type mvp-vm \
  --machine-type n1-standard-4
```

### **Horizontal Scaling (More Instances):**
```bash
# Cloud Run (automatic)
gcloud run services update mvp-rag \
  --max-instances 10 \
  --min-instances 1
```

---

## 🛠️ Troubleshooting

### **Common Issues:**

**1. Port Already in Use:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**2. Permission Denied:**
```bash
# Fix permissions
chmod +x run.sh
chmod +x main.py
```

**3. Module Not Found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Support

- **Documentation**: `docs/README.md`
- **Issues**: Check `TEST_RESULTS.md`
- **Deployment**: This guide

---

**🚀 Your MVP is ready for production deployment!**
