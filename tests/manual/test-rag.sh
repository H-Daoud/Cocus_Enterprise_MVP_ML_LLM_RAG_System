#!/bin/bash
# Test 4: RAG Query
echo "🧪 Testing: RAG Query Endpoint"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Sending test query..."
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query":"What is machine learning?","include_sources":true}' \
  2>/dev/null | python3 -m json.tool
echo ""
echo "✅ Expected: Should return answer and sources (if API key configured)"
