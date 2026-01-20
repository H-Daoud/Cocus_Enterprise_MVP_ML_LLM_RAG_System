# 🚀 Quick Start Guide for Testers & PMs

## ⚡ **Super Fast Setup (2 Minutes)**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/COCUS-MVP_ML_LLM_RAG_System.git
cd COCUS-MVP_ML_LLM_RAG_System
```

### **Step 2: Run Automated Setup**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

That's it! The script will:
- ✅ Check prerequisites (Python, Docker)
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Configure environment variables
- ✅ Run tests
- ✅ Guide you through API key setup

### **Step 3: Start the Application**
```bash
./scripts/run.sh
```

### **Step 4: Test It!**
Open your browser: **http://localhost:8000/api/docs**

### **Step 5: Run Automated Tests (Optional)**
```bash
./scripts/utils/test-all.sh
```

This will automatically test:
- ✅ Health checks
- ✅ API endpoints
- ✅ Data validation
- ✅ RAG functionality
- ✅ GDPR compliance
- ✅ EU AI Act compliance
- ✅ Performance

**Expected output:** `✅ ALL TESTS PASSED!`

### **Step 6: Open Chat UI for PM Testing (Optional)**
```bash
./scripts/open-chat.sh
```

This opens a beautiful web interface where PMs can:
- 💬 Chat with the RAG system
- 📊 See real-time responses
- 📚 View source citations
- ✅ Test without command line

**Or open directly:** `file://$(pwd)/frontend/chat-ui.html`

---

## 🎯 **What You Can Test**

### **1. Health Check**
```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "system": {...}
}
```

### **2. Data Validation**
Upload the sample data file:
```bash
curl -X POST "http://localhost:8000/api/validation/validate" \
  -F "file=@data/raw/orders_sample.ndjson"
```

**What it tests:**
- ✅ Pydantic data validation
- ✅ Business rules enforcement
- ✅ GDPR compliance (PII anonymization)
- ✅ EU AI Act compliance (audit logging)

### **3. RAG Chat (Requires Gemini API Key)**
```bash
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

**What it tests:**
- ✅ Google Gemini integration
- ✅ LLM response generation
- ✅ Source citations (transparency)

---

## 🔑 **API Key Setup (Optional)**

### **Option 1: Use Gemini (FREE)**
1. Get FREE API key: https://makersuite.google.com/app/apikey
2. Add to `.env` file:
   ```bash
   GEMINI_API_KEY=your_key_here
   LLM_PROVIDER=gemini
   ```

### **Option 2: Use Mock Mode (No API Key)**
Perfect for testing without AI:
```bash
# In .env file
LLM_PROVIDER=mock
```

---

## 🐳 **Alternative: Docker Setup**

If you prefer Docker:

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

**Services included:**
- 🌐 API (port 8000)
- 🗄️ PostgreSQL (port 5432)
- 🔴 Redis (port 6379)
- 📊 MLflow (port 5000)
- 📈 Grafana (port 3001)
- 🔍 Prometheus (port 9090)

---

## 📊 **Testing Checklist**

### **Basic Functionality**
- [ ] API starts without errors
- [ ] Health endpoint returns 200
- [ ] API documentation loads
- [ ] Data validation works
- [ ] RAG query returns response

### **Enterprise Features**
- [ ] GDPR anonymization works
- [ ] EU AI Act audit logs generated
- [ ] Prometheus metrics exposed
- [ ] Error handling works properly

### **Performance**
- [ ] API responds in < 1 second
- [ ] Can handle 10 concurrent requests
- [ ] Memory usage is reasonable

---

## 🆘 **Troubleshooting**

### **Issue: "Module not found"**
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### **Issue: "Port 8000 already in use"**
**Solution:**
```bash
pkill -f uvicorn
./scripts/run.sh
```

### **Issue: "API key not working"**
**Solution:**
1. Check `.env` file has correct key
2. Verify key starts with `AIza`
3. Try mock mode: `LLM_PROVIDER=mock`

### **Issue: "Tests failing"**
**Solution:**
```bash
pytest tests/unit/ -v
# Check TEST_RESULTS.md for details
```

---

## 📚 **Documentation**

| Document | Purpose |
|----------|---------|
| `README.md` | Full project documentation |
| `docs/internal_summaries/SETUP_GUIDE.md` | Detailed setup instructions |
| `docs/internal_summaries/GEMINI_SETUP.md` | Gemini API configuration |
| `docs/internal_summaries/ENV_VARIABLES_GUIDE.md` | Environment variables |
| `docs/internal_summaries/ENTERPRISE_QUICK_REFERENCE.txt` | Quick commands |
| `docs/internal_summaries/TEST_RESULTS.md` | Latest test results |

---

## 🎯 **For Product Managers**

### **What to Focus On:**

1. **Data Validation Dashboard**
   - Upload `data/raw/orders_sample.ndjson`
   - See validation results
   - Check error handling

2. **RAG Chat Interface**
   - Test natural language queries
   - Verify source citations
   - Check response quality

3. **Compliance Features**
   - GDPR: PII anonymization
   - EU AI Act: Audit logging
   - Transparency: Source citations

### **Demo Script:**

```bash
# 1. Start the system
./scripts/run.sh

# 2. Open API docs
open http://localhost:8000/api/docs

# 3. Test health
curl http://localhost:8000/api/health

# 4. Test validation
curl -X POST "http://localhost:8000/api/validation/validate" \
  -F "file=@data/raw/orders_sample.ndjson"

# 5. Test RAG
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain data validation"}'
```

---

## ⏱️ **Estimated Testing Time**

- **Quick Test:** 5 minutes
- **Full Test:** 30 minutes
- **Deep Dive:** 2 hours

---

## ✅ **Success Criteria**

Your test is successful if:
- ✅ API starts without errors
- ✅ All health checks pass
- ✅ Data validation works
- ✅ RAG returns responses (with or without API key)
- ✅ No critical errors in logs

---

## 🚀 **Ready to Test!**

1. Run `./scripts/setup.sh`
2. Run `./scripts/run.sh`
3. Open http://localhost:8000/api/docs
4. Start testing!

**Questions?** Check the documentation or create an issue on GitHub.

---

**Happy Testing! 🎉**
