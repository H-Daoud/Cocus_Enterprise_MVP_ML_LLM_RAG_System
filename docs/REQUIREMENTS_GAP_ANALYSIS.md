# MVP Requirements Analysis & Gap Assessment

## Overview
This document maps the official PDF requirements (Part 1 & Part 2) to the current implementation status.

---

## PART 1: Data Validation Challenge

### ✅ **COMPLETED Requirements:**

1. **Pydantic Models** ✅
   - Location: `src/models/order.py`
   - Status: Complete with all field validations

2. **NDJSON Ingestion** ✅
   - Location: `src/rag/manager.py` (load_ndjson method)
   - Status: Working, processes all 50 orders

3. **Normalization vs Rejection** ✅
   - Implemented in: `src/data_validation/validator.py`
   - Auto-corrects: String booleans, type coercion
   - Hard failures: Negative quantities, invalid emails

### ❌ **MISSING Requirements:**

#### 4. **Data Quality Analysis** (NOT DONE)
Required analysis questions:

1. **Overall Acceptance Rate**
   - ❌ Not calculated
   - Need: Script to compute accepted vs rejected ratio

2. **Per-Field Basic Profiles**
   - ❌ Not generated
   - Need: Counts, distinct values, min/max for key fields

3. **Missing/Unusable Values**
   - ❌ Not reported
   - Need: Count of missing values per column

4. **Outliers and Extreme Values**
   - ❌ Not identified
   - Need: Min/max analysis, extreme value detection

5. **Quality by Grouping**
   - ❌ Not done
   - Need: Acceptance rate per category (e.g., by status, country)

#### 5. **Output Documentation** (PARTIAL)
- ✅ Pydantic models exported
- ✅ Validation script exists
- ❌ **Missing**: Formal summary document answering all analysis questions

---

## PART 2: LLM-RAG Challenge

### ✅ **COMPLETED Requirements:**

1. **OpenAI-Compatible API** ✅
   - Using: Hugging Face Router
   - Environment vars: OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL_NAME

2. **Reuse Validated Orders** ✅
   - Loading from: `data/raw/orders_sample.ndjson`
   - Integration: RAGManager processes accepted records

3. **Simple In-Memory Index** ✅
   - Using: ChromaDB (vector store)
   - Embeddings: HuggingFace sentence-transformers
   - Similarity: Cosine similarity via ChromaDB

4. **Text Documents per Order** ✅
   - Location: `src/rag/manager.py` (load_ndjson)
   - Format: Includes order_id, customer, status, shipping, quantity, price, tags, coupon

5. **Retrieval Tool** ✅
   - Location: `src/rag/manager.py` (query method)
   - Hybrid Search: Vector + Exact key matching

### ❌ **MISSING Requirements:**

#### 6. **pydantic-ai Agent** (NOT IMPLEMENTED)
Required components:

- ❌ **Output Schema**: Structured Pydantic model with:
  - `answer: str`
  - `used_order_ids: List[str]`
  - `confidence: float`

- ❌ **Agent Definition**: pydantic-ai agent (currently using raw LangChain)

- ❌ **System Prompt**: Explicit instructions to:
  - Use only retrieved documents as evidence
  - Not invent order IDs
  - Always fill `used_order_ids`

#### 7. **Answer 3 Core Business Questions** (PARTIAL)

**Question 1: Per-Order Explanation (ORD-0003)**
- ✅ Can retrieve ORD-0003
- ❌ No structured output with `used_order_ids`
- ❌ No data quality perspective in response

**Question 2: Coupon and Tag Patterns**
- ✅ Can search for coupons/tags
- ❌ No pattern analysis
- ❌ No structured output

**Question 3: Suspicious/Edge Cases**
- ✅ Can retrieve orders
- ❌ No automatic edge-case detection
- ❌ No business rule analysis

#### 8. **Deliverables** (PARTIAL)

- ✅ Code for loading validated orders
- ✅ Document text building
- ✅ Embeddings and index
- ❌ **pydantic-ai agent definition**
- ❌ **Entry point script** that runs all 3 questions
- ❌ **Prints structured output** (answer + used_order_ids)

---

## Critical Gaps for Presentation

### **Must Implement Before Presentation:**

1. **Data Quality Analysis Report** (Part 1, Question 5)
   - Script: `scripts/data_quality_analysis.py`
   - Output: `reports/data_quality_report.md`

2. **pydantic-ai Agent** (Part 2, Requirement 3)
   - File: `src/agents/order_agent.py`
   - Structured output with `used_order_ids`

3. **3 Business Questions Script** (Part 2, Requirement 4)
   - File: `scripts/run_business_questions.py`
   - Prints structured answers for all 3 questions

4. **Presentation Demo Script**
   - File: `demo_presentation.py`
   - Shows live execution of all requirements

---

## Recommended Implementation Order

### **Priority 1: Data Quality Analysis (2 hours)**
1. Create `scripts/data_quality_analysis.py`
2. Answer all 5 analysis questions
3. Generate `reports/data_quality_report.md`

### **Priority 2: pydantic-ai Agent (2 hours)**
1. Install `pydantic-ai`
2. Create structured output schema
3. Implement agent with retrieval tool
4. Test with 3 business questions

### **Priority 3: Demo Script (1 hour)**
1. Create `demo_presentation.py`
2. Combine Part 1 analysis + Part 2 Q&A
3. Test end-to-end flow

---

## Current System Strengths

✅ **Working Components:**
- Hybrid Search (Vector + Exact matching)
- NDJSON ingestion
- Pydantic validation models
- RAG retrieval pipeline
- Professional UI
- Docker deployment ready

**These don't need to change!** We just need to add the missing analysis and pydantic-ai layer.
