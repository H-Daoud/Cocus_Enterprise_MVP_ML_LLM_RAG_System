#!/bin/bash
# Test 1: Health Check
echo "🧪 Testing: Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s http://localhost:8000/api/health | python3 -m json.tool
echo ""
echo "✅ Expected: status should be 'healthy'"
