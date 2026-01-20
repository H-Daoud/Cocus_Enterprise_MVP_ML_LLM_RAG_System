# 📁 Simplified Project Structure

**Clean, organized structure for easy navigation**

---

## 🎯 Core Files (What You Need)

```
COCUS-MVP_ML_LLM_RAG_System/
│
├── main.py                    ← RUN THIS! (Master orchestrator)
├── README.md                  ← Project overview
├── requirements.txt           ← Python dependencies
│
├── docs/                      ← 📚 ALL DOCUMENTATION HERE
│   ├── README.md              ← Documentation index
│   ├── COMPLETE_REQUIREMENTS_QA.md  ← For PM review ⭐
│   ├── PRESENTATION_README.md       ← For presentation
│   ├── DOCKER_DEPLOYMENT.md         ← Deployment guide
│   └── GITHUB_ACTIONS_GUIDE.md      ← CI/CD guide
│
├── src/                       ← Source code
│   ├── models/order.py        ← Pydantic models
│   ├── rag/manager.py         ← RAG system
│   └── privacy/gdpr_masking.py ← GDPR compliance
│
├── scripts/                   ← Executable scripts
│   ├── process_data_gdpr.py   ← GDPR workflow
│   ├── data_quality_analysis.py
│   ├── train_ml_model_real.py
│   └── run_business_questions.py
│
├── notebooks/                 ← Jupyter notebooks
│   └── Complete_ML_Pipeline_Andrew_Ng.ipynb
│
├── models/                    ← Trained ML models
│   ├── anomaly_detection.onnx
│   ├── anomaly_detection.pkl
│   └── anomaly_detection_metadata.json
│
├── data/                      ← Data files
│   ├── raw/orders_sample.ndjson
│   ├── processed/orders_masked.ndjson
│   └── vectorstore/           ← RAG index
│
└── reports/                   ← Generated reports
    └── data_quality_report.md
```

---

## 🗂️ Folder Purpose

| Folder | Purpose | Key Files |
|--------|---------|-----------|
| **`docs/`** | All documentation | Q&A, guides, PDFs |
| **`src/`** | Source code | Models, RAG, privacy |
| **`scripts/`** | Executable scripts | Data processing, ML training |
| **`notebooks/`** | Jupyter notebooks | ML pipeline demo |
| **`models/`** | Trained models | ONNX, PKL, metadata |
| **`data/`** | Data files | Raw, processed, vectorstore |
| **`reports/`** | Generated reports | Quality analysis |

---

## 🚀 Quick Actions

### **Run Complete Pipeline:**
```bash
python3 main.py
```

### **View Documentation:**
```bash
cd docs/
open README.md  # Documentation index
```

### **Start Chat UI:**
```bash
./run.sh
```

### **Train ML Model:**
```bash
python3 scripts/train_ml_model_real.py
```

---

## 📚 Documentation Locations

All docs are in `docs/` folder:

1. **`README.md`** - Documentation index
2. **`COMPLETE_REQUIREMENTS_QA.md`** - PM review (25 Q&A)
3. **`PRESENTATION_README.md`** - Presentation guide
4. **`DOCKER_DEPLOYMENT.md`** - Deployment
5. **`GITHUB_ACTIONS_GUIDE.md`** - CI/CD

---

## 🎯 For Presentation

**Everything you need:**
1. Run: `python3 main.py`
2. Review: `docs/COMPLETE_REQUIREMENTS_QA.md`
3. Demo: `notebooks/Complete_ML_Pipeline_Andrew_Ng.ipynb`
4. UI: `./run.sh` → http://localhost:8000/chat-ui.html

---

## ✅ Simplified!

**Before**: Docs scattered everywhere  
**After**: All docs in `docs/` folder

**Before**: Complex structure  
**After**: Clear, simple organization

**Before**: Hard to find files  
**After**: Everything documented here

---

**📍 Current location**: Project root  
**📍 Documentation**: `docs/` folder  
**📍 Main script**: `main.py`
