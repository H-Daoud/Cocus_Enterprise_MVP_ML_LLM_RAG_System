# Logs & Monitoring - COCUS MVP

## 📝 Logging System

The COCUS MVP uses a centralized, structured logging system to ensure observability across all components (API, RAG, and ML).

### Log Structure
Logs are categorized into four main areas, located in the root `logs/` directory:

| Directory | Description |
|-----------|-------------|
| `logs/app/` | Application-level logs (API startup, routing, errors). |
| `logs/audit/` | Compliance and security audit trails (GDPR masking, access). |
| `logs/ml/` | Machine learning logs (training metrics, drift detection). |
| `logs/security/` | Security-related logs (unauthorized access attempts). |

### Logging Implementation (`src/utils/logger.py`)
- **JSON Formatting**: Logs can be output in JSON format for easy ingestion by log aggregators (ELK, Datadog).
- **Standard Formatting**: Traditional human-readable logs for local development.
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL.

---

## 📊 Monitoring system

Monitoring is built into the API layer to provide real-time insights into system health and performance.

### Prometheus Metrics
The API exposes high-fidelity metrics for Prometheus at the `/metrics` endpoint.

**Key Metrics Tracked**:
- **HTTP Request Latency**: Response times for all API endpoints.
- **Request Count**: Total number of successfully processed requests.
- **Error Rate**: 4xx and 5xx response frequency.
- **System Health**: Uptime and memory usage.

### Grafana Dashboards
Placeholder configurations for Grafana can be found in `monitoring/grafana/`. These dashboards are designed to visualize:
1. **API Throughput**: Requests per second.
2. **Model Performance**: Inference latency and anomaly rates.
3. **Data Quality**: Acceptance/rejection rates from the validation layer.

---

## ⚖️ Compliance Logging (Audit Trail)

To satisfy **EU AI Act** and **GDPR** requirements, the system maintains a dedicated audit trail in `logs/audit/`.

- **Citations**: The RAG agent's citations are logged to ensure transparency.
- **Privacy**: No PII is logged. The masking utility ensures that only anonymized IDs appear in the log files.
- **Retention**: Audit logs are designed for long-term retention as required by legal standards.
