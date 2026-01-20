#!/bin/bash
# Test 5: GDPR Anonymization
echo "🧪 Testing: GDPR PII Anonymization"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'EOF'
from src.models.order import Order

# Create test order
order = Order(
    order_id="TEST-GDPR-001",
    customer_email="john.doe@example.com",
    quantity=2,
    unit_price=29.99,
    is_gift=False,
    status="pending",
    created_at="2025-01-15T10:30:00Z",
    shipping={
        "country_code": "US",
        "city": "New York",
        "postal_code": "10001"
    },
    priority=3
)

print(f"Original Email: {order.customer_email}")

# Test anonymization
anonymized = order.anonymize_pii()
print(f"Anonymized Email: {anonymized.customer_email}")

# Verify
if "anonymized" in anonymized.customer_email:
    print("\n✅ GDPR Anonymization PASSED")
else:
    print("\n❌ GDPR Anonymization FAILED")
EOF
echo ""
echo "✅ Expected: Email should be anonymized (e.g., anonymized@example.com)"
