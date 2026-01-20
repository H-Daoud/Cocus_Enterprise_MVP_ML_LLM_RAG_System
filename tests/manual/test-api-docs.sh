#!/bin/bash
# Test 2: API Documentation
echo "🧪 Testing: API Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Opening API documentation in browser..."
open http://localhost:8000/api/docs 2>/dev/null || xdg-open http://localhost:8000/api/docs 2>/dev/null || echo "Please open: http://localhost:8000/api/docs"
echo ""
echo "✅ Expected: Swagger UI should load with interactive API documentation"
