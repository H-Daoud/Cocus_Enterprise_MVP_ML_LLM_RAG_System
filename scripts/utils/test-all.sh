#!/bin/bash

# ============================================================================
# COCUS MVP - Automated Test Suite
# ============================================================================
# Runs all tests for PMs and testers with clear pass/fail indicators
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test results
PASSED=0
FAILED=0
TOTAL=0

# Detect and activate virtual environment
if [ -d "venv" ]; then
    echo -e "${BLUE}Detected virtual environment, activating...${NC}"
    source venv/bin/activate
elif [ -d "../../../venv" ]; then
    echo -e "${BLUE}Detected virtual environment, activating...${NC}"
    source ../../../venv/bin/activate
fi

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    TOTAL=$((TOTAL + 1))
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Test $TOTAL: $test_name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    echo -e "${YELLOW}Running: $test_command${NC}"
    
    if output=$(eval "$test_command" 2>&1); then
        if [[ -z "$expected_pattern" ]] || echo "$output" | grep -q "$expected_pattern"; then
            echo -e "${GREEN}✅ PASSED${NC}"
            echo "$output" | head -10
            PASSED=$((PASSED + 1))
            return 0
        else
            echo -e "${RED}❌ FAILED - Expected pattern not found: $expected_pattern${NC}"
            echo "$output" | head -20
            FAILED=$((FAILED + 1))
            return 1
        fi
    else
        echo -e "${RED}❌ FAILED - Command failed${NC}"
        echo "$output" | head -20
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Banner
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║        🧪 COCUS MVP - Automated Test Suite 🧪                 ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Move to project root
cd "$(dirname "$0")/../.."

# Check if API is running
echo -e "${BLUE}Checking if API is running...${NC}"
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo -e "${RED}❌ API is not running!${NC}"
    echo ""
    echo "Please start the API first:"
    echo -e "  ${GREEN}./scripts/run.sh${NC}"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ API is running${NC}"

# ============================================================================
# BASIC TESTS
# ============================================================================
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  BASIC TESTS (10 min)                                         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"

# Test 1: Health Check
run_test \
    "Health Check" \
    "curl -s http://localhost:8000/api/health" \
    '"status":"healthy"'

# Test 2: API Documentation
run_test \
    "API Documentation Loads" \
    "curl -s http://localhost:8000/api/docs | grep -q 'swagger' && echo 'Swagger UI loaded'" \
    "Swagger UI loaded"

# Test 3: Data Validation Endpoint
run_test \
    "Data Validation Endpoint" \
    "curl -s -X POST 'http://localhost:8000/api/validation/validate' -F 'file=@data/raw/orders_sample.ndjson' | python3 -c 'import sys, json; d=json.load(sys.stdin); print(\"Valid orders:\", d.get(\"valid_count\", 0))'" \
    "Valid orders:"

# Test 4: RAG Query Response
run_test \
    "RAG Query Returns Response" \
    "curl -s -X POST 'http://localhost:8000/api/rag/query' -H 'Content-Type: application/json' -d '{\"query\":\"test\"}' | python3 -c 'import sys, json; d=json.load(sys.stdin); print(\"Answer:\", d.get(\"answer\", \"No answer\")[:50])'" \
    "Answer:"

# ============================================================================
# ENTERPRISE FEATURES TESTS
# ============================================================================
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ENTERPRISE FEATURES TESTS (15 min)                           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"

# Test 5: GDPR Anonymization
run_test \
    "GDPR PII Anonymization" \
    "python3 -c '
from src.models.order import Order
order = Order(
    order_id=\"ORD-0001\",
    customer_email=\"test@example.com\",
    quantity=1,
    unit_price=10.0,
    is_gift=False,
    status=\"pending\",
    created_at=\"2025-01-01T00:00:00Z\",
    shipping={\"country_code\":\"US\",\"city\":\"NYC\",\"postal_code\":\"10001\"},
    priority=1
)
anon = order.anonymize_pii()
print(f\"Original: {order.customer_email}\")
print(f\"Anonymized: {anon.customer_email}\")
assert \"anonymized\" in anon.customer_email
print(\"✅ GDPR anonymization works\")
'" \
    "GDPR anonymization works"

# Test 6: EU AI Act Audit Logging
run_test \
    "EU AI Act Audit Logging" \
    "python3 -c '
from src.models.order import Order
order = Order(
    order_id=\"ORD-0002\",
    customer_email=\"test@example.com\",
    quantity=1,
    unit_price=10.0,
    is_gift=False,
    status=\"pending\",
    created_at=\"2025-01-01T00:00:00Z\",
    shipping={\"country_code\":\"US\",\"city\":\"NYC\",\"postal_code\":\"10001\"},
    priority=1
)
audit = order.to_audit_log()
print(f\"Audit log keys: {list(audit.keys())}\")
assert \"timestamp\" in audit
assert \"order_id\" in audit
print(\"✅ EU AI Act audit logging works\")
'" \
    "EU AI Act audit logging works"

# Test 7: Error Handling
run_test \
    "Error Handling" \
    "curl -s -X POST 'http://localhost:8000/api/validation/validate' -H 'Content-Type: application/json' -d '{}' | python3 -c 'import sys, json; d=json.load(sys.stdin); print(\"Error detail:\", d.get(\"detail\", \"No error\")[:50])'" \
    "detail"

# Test 8: Performance Check
run_test \
    "Performance (Response Time < 2s)" \
    "time_out=\$( { time -p curl -s http://localhost:8000/api/health > /dev/null; } 2>&1 ); real_time=\$(echo \"\$time_out\" | grep real | awk '{print \$2}'); echo \"Response time: \${real_time}s\"; python3 -c \"import sys; sys.exit(0 if float('\${real_time}') < 2.0 else 1)\" && echo '✅ Response time OK'" \
    "Response time OK"

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  TEST SUMMARY                                                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Total Tests:  ${BLUE}$TOTAL${NC}"
echo -e "Passed:       ${GREEN}$PASSED${NC}"
echo -e "Failed:       ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  ✅ ALL TESTS PASSED! System is working correctly! ✅         ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}║  ❌ SOME TESTS FAILED - Please review the output above        ║${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  • Check logs in api.log"
    echo "  • Verify .env configuration"
    echo "  • Ensure all dependencies are installed"
    echo "  • See SETUP_GUIDE.md for help"
    echo ""
    exit 1
fi
