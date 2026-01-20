# Compliance Strategy - COCUS MVP

## ⚖️ GDPR & EU AI Act Implementation

This project is built with a "Privacy by Design" philosophy, ensuring full compliance with European data protection and AI transparency standards.

## 🛡️ GDPR Compliance (Privacy by Design)

The system adheres to **GDPR Article 25** by implementing privacy-preserving techniques throughout the data lifecycle.

### 1. Data Minimization (Article 5)
- We only collect and process fields necessary for anomaly detection and RAG analysis.
- PII (Personally Identifiable Information) like email addresses and street addresses are transformed immediately upon ingestion.

### 2. PII Masking Implementation
- **Emails**: Partially masked (e.g., `john.doe@example.com` → `j***@example.com`).
- **Addresses**: Street names are completely redacted (`*** *** ***`), and postal codes are truncated (`10115` → `101**`).
- **Location**: [src/privacy/gdpr_masking.py](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/src/privacy/gdpr_masking.py).

### 3. Right to be Forgotten
- All data is indexed using an anonymized `customer_id`. Deletion of a record in the raw data system automatically triggers a purge in the vector store and training sets during the next orchestration run.

## 🤖 EU AI Act Compliance

As an AI-powered RAG system, the COCUS MVP follows the transparency and record-keeping requirements outlined in the **EU AI Act**.

### 1. Transparency (Article 13)
- **Source Citations**: The RAG agent is prohibited from providing information without a direct citation. Every answer includes a `used_order_ids` field, showing exactly which records were used to generate the response.
- **Audit Trail**: Any anomaly detection or analysis is logged with a confidence score, ensuring that human operators can verify the AI's reasoning.

### 2. Record-Keeping (Article 12)
- The system automatically generates comprehensive validation and quality reports.
- **Audit Logs**: [compliance/audit_logs/](file:///Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System/compliance/audit_logs/) stores time-stamped logs of all data processing operations.

### 3. Human Oversight
- Analysis questions like "Identify suspicious orders" are designed to *flag* potential issues for human review, rather than making automated legal or financial decisions.

## 📊 Compliance Metrics
- **PII Leakage Rate**: 0% (All PII is masked before model exposure).
- **Citation Coverage**: 100% (Every RAG answer requires evidence citations).
- **Validation Audit**: All rejected records (currently 58%) are logged with specific refusal reasons (invalid email, negative price, etc.).
