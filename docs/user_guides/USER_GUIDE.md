# User Guide - COCUS MVP

## 👋 Welcome to the COCUS RAG System

This guide is designed for business analysts, product managers, and users who want to interact with the system without diving into the source code.

## 💬 Interacting with the Chat UI

The easiest way to use the system is through the **Chat Interface**.

### How to access:
1. Ensure the system is running (`./run.sh`).
2. Open your browser and navigate to: `http://localhost:8000/chat-ui.html`
3. Or run the convenience script: `./open-chat.sh`

### What you can ask:
- **Specific Order Inquiries**: "Explain what happened with order ORD-0003."
- **Trend Analysis**: "What are the common tags used in successful orders?"
- **Fraud/Anomaly Detection**: "Identify any suspicious orders and explain why."

## 🔌 API for Advanced Users

If you are a developer or data analyst, you can interact directly with the FastAPI endpoints.

### 1. Interactive Documentation
Access the auto-generated Swagger UI at: `http://localhost:8000/api/docs`

### 2. Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check system status |
| `/api/query` | POST | Ask a RAG question (JSON body) |
| `/api/validation/validate` | POST | Upload and validate a data file |

### 3. Example Query (via Curl)
```bash
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me all orders from Portugal that have coupons."}'
```

## 📊 Understanding Results

### Source Citations
Every answer produced by the AI will list the **Order IDs** it used as evidence. You can verify these IDs manually in the data files to ensure accuracy.

### Confidence Scores
The AI provides a confidence score (0.0 to 1.0). 
- **> 0.8**: Highly reliable.
- **0.5 - 0.8**: Reliable but review the citations.
- **< 0.5**: Interpret with caution; the AI may not have found enough context.

## ❓ FAQ

**Q: Why was my order rejected?**
A: All rejected orders are logged with a reason. Common reasons include "Invalid Email Format" or "Positive Quantity Required."

**Q: Can I use this with my own data?**
A: Yes! Place your NDJSON file in `data/raw/` and restart the system.

**Q: Is my data safe?**
A: Yes. All sensitive fields (emails, addresses) are masked before they are processed by the AI or stored in the database.
