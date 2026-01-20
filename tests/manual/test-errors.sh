#!/bin/bash
# Test 7: Error Handling
echo "🧪 Testing: Error Handling"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Sending invalid request (missing file)..."
curl -X POST "http://localhost:8000/api/validation/validate" \
  -H "Content-Type: application/json" \
  -d '{}' \
  2>/dev/null | python3 -m json.tool
echo ""
echo "✅ Expected: Should return clear error message with 422 status"
