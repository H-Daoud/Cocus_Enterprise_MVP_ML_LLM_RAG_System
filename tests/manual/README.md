# Manual Test Scripts

Individual test scripts for easy one-click testing.

## Usage

Each script can be run independently:

```bash
# Run individual tests
./tests/manual/test-health.sh
./tests/manual/test-api-docs.sh
./tests/manual/test-validation.sh
./tests/manual/test-rag.sh
./tests/manual/test-gdpr.sh
./tests/manual/test-audit.sh
./tests/manual/test-errors.sh
./tests/manual/test-performance.sh
```

Or run all tests at once:

```bash
./test-all.sh
```

## Test Descriptions

| Test | Script | What It Tests |
|------|--------|---------------|
| **Health Check** | `test-health.sh` | API is running and healthy |
| **API Documentation** | `test-api-docs.sh` | Swagger UI loads correctly |
| **Data Validation** | `test-validation.sh` | Order validation endpoint works |
| **RAG Query** | `test-rag.sh` | AI query responses |
| **GDPR Anonymization** | `test-gdpr.sh` | PII protection |
| **EU AI Act Audit** | `test-audit.sh` | Compliance logging |
| **Error Handling** | `test-errors.sh` | Error responses |
| **Performance** | `test-performance.sh` | Response time < 2s |

## Requirements

- API must be running (`./run.sh`)
- Virtual environment activated
- Sample data in `data/raw/orders_sample.ndjson`

## Expected Results

Each test will show:
- ✅ PASSED - Test succeeded
- ❌ FAILED - Test failed
- Clear output showing what was tested
- Expected vs actual results
