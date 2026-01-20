#!/bin/bash
# Test 6: EU AI Act Audit Logging
echo "🧪 Testing: EU AI Act Audit Logging"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'EOF'
from src.models.order import Order
import json

# Create test order
order = Order(
    order_id="TEST-AUDIT-001",
    customer_email="test@example.com",
    quantity=1,
    unit_price=49.99,
    is_gift=True,
    status="completed",
    created_at="2025-01-15T14:20:00Z",
    shipping={
        "country_code": "DE",
        "city": "Berlin",
        "postal_code": "10115"
    },
    priority=1
)

# Generate audit log
audit_log = order.to_audit_log()

print("Audit Log Generated:")
print(json.dumps(audit_log, indent=2))

# Verify required fields
required_fields = ["timestamp", "order_id", "action", "data"]
missing = [f for f in required_fields if f not in audit_log]

if not missing:
    print("\n✅ EU AI Act Audit Logging PASSED")
else:
    print(f"\n❌ EU AI Act Audit Logging FAILED - Missing: {missing}")
EOF
echo ""
echo "✅ Expected: Audit log should contain timestamp, order_id, action, and data"
