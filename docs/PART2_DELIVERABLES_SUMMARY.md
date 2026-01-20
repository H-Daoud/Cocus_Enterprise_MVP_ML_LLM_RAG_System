# 📄 Part 2 Deliverables Summary

This document summarizes the deliverables for **Challenge LLM-RAG Part 2**, ensuring all requirements for the PM review are met.

---

## 1. Code Deliverables

| Requirement | Implementation | File Link |
|-------------|----------------|-----------|
| **Loading Validated Orders** | `RAGManager.load_ndjson()` parses `.ndjson` files from Part 1. | [manager.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/src/rag/manager.py#L41) |
| **Building Document Texts** | Structured text representation for better retrieval. | [manager.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/src/rag/manager.py#L60) |
| **Embeddings & Indexing** | Uses `HuggingFaceEmbeddings` and `ChromaDB`. | [manager.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/src/rag/manager.py#L135) |
| **Pydantic-AI Agent** | Agent definition with structured output and tool registry. | [run_business_questions.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/scripts/run_business_questions.py#L68) |
| **Output Schema** | `OrderAnalysisOutput` with `used_order_ids`. | [run_business_questions.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/scripts/run_business_questions.py#L24) |
| **Retrieval Tool** | `search_orders_tool` integration. | [run_business_questions.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/scripts/run_business_questions.py#L98) |
| **Simple Entry Point** | Script that builds index, runs questions, and prints results. | [run_business_questions.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/scripts/run_business_questions.py) |

---

## 2. Configuration (`.env`)

The system expects the following environment variables (defined in `.env.template`):

```bash
# HuggingFace / OpenAI compatible API Configuration
OPENAI_API_KEY=hf_your_token_here
OPENAI_API_BASE=https://router.huggingface.co/v1
OPENAI_MODEL=meta-llama/Llama-3.2-3B-Instruct
```

> [!NOTE]
> We use the **HuggingFace OpenAI-compatible Router** to access Llama 3.2. This allows us to use standard OpenAI client libraries with the Llama model.

---

## 3. Short Notes

### **Data Handover (Part 1 to Part 2)**
Part 2 expects a directory of `.ndjson` files located in `data/raw/` or `data/processed/`. The `RAGManager` automatically scans these folders and performs bulk indexing.

### **Document Format & Indexing**
- **Format**: Each order is transformed into a descriptive text block (e.g., `ORDER_SEARCH_ID: ORD-0001 ... Status: pending`).
- **Index**: We use **ChromaDB** with **HuggingFace Embeddings** (`sentence-transformers/all-MiniLM-L6-v2`).
- **Search**: Hybrid search is implemented (Semantic Similarity + Exact ID matching fallback).

### **Limitations & Shortcuts**
1. **Fixed K**: The agent retrieves a fixed $K=10$ results per query for stability.
2. **Temperature**: Hardcoded to `0.7` to balance creativity and factual consistency.
3. **Async Tools**: Pydantic-AI tools are implemented as `async` to prevent blocking the event loop.
4. **Context Window**: For this MVP, we assume the retrieved context fits within the model's window (~128k for Llama-3.2).

---

## 🚀 How to Run Part 2 Deliverables

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.template .env
# Add your key to .env

# 3. Run the entry point script
python3 scripts/run_business_questions.py
```

---
**Status**: Part 2 Deliverables Complete ✅
