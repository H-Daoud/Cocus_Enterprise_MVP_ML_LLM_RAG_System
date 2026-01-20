#!/bin/bash
# Test 8: Performance
echo "🧪 Testing: Performance (Response Time)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Measuring response time for health endpoint..."
echo ""

# Measure time
START=$(date +%s.%N)
curl -s http://localhost:8000/api/health > /dev/null
END=$(date +%s.%N)

# Calculate duration
DURATION=$(echo "$END - $START" | bc)

echo "Response Time: ${DURATION}s"
echo ""

# Check if under 2 seconds
if (( $(echo "$DURATION < 2.0" | bc -l) )); then
    echo "✅ Performance PASSED (< 2 seconds)"
else
    echo "❌ Performance FAILED (>= 2 seconds)"
fi

echo ""
echo "✅ Expected: Response time should be < 2 seconds"
