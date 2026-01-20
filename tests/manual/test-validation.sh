#!/bin/bash
# Test 3: Data Validation
echo "🧪 Testing: Data Validation Endpoint"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Uploading sample data file..."
curl -X POST "http://localhost:8000/api/validation/validate" \
  -F "file=@data/raw/orders_sample.ndjson" \
  2>/dev/null | python3 -m json.tool
echo ""
echo "✅ Expected: Should show valid_count and invalid_count"
