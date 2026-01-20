#!/bin/bash

# ============================================================================
# COCUS MVP - Re-index Orders
# ============================================================================
# Re-processes the NDJSON data into the vector store
# ============================================================================

set -e

# Move to project root
cd "$(dirname "$0")/.."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔄 Re-indexing order data...${NC}"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️  Virtual environment not found. Please run setup.sh first.${NC}"
    exit 1
fi

# Set PYTHONPATH and run indexer
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 scripts/index_documents.py

echo ""
echo -e "${GREEN}✅ Indexing complete! Your assistant is now up to date with the latest data.${NC}"
echo ""
