#!/bin/bash

# ============================================================================
# COCUS MVP - Open Chat UI
# ============================================================================
# Opens the RAG chat interface in the default browser
# ============================================================================

# Move to project root
cd "$(dirname "$0")/.."

echo "🚀 Opening RAG Chat Interface..."
echo ""

# Check if API is running
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "⚠️  API is not running!"
    echo ""
    echo "Please start the API first:"
    echo "  ./run.sh"
    echo ""
    exit 1
fi

echo "✅ API is running"
echo "✅ Opening chat interface in browser..."
echo ""

# Get the full path to the HTML file
HTML_FILE="$(pwd)/frontend/chat-ui.html"

# Open in default browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$HTML_FILE"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$HTML_FILE"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    start "$HTML_FILE"
else
    echo "Please open this file in your browser:"
    echo "  file://$HTML_FILE"
fi

echo ""
echo "📖 Chat UI opened!"
echo ""
echo "You can also access it directly:"
echo "  file://$(pwd)/frontend/chat-ui.html"
echo ""
echo "Or via the API documentation:"
echo "  http://localhost:8000/api/docs"
echo ""
