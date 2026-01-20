#!/bin/bash

# ============================================================================
# COCUS MVP - Quick Run Script
# ============================================================================
# Starts the API server with proper configuration
# ============================================================================

set -e

# Move to project root
cd "$(dirname "$0")/.."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${BLUE}🚀 Starting COCUS MVP API Server...${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Running setup first...${NC}"
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Running setup first...${NC}"
    ./setup.sh
fi

# Kill any existing uvicorn processes
pkill -f "uvicorn src.api.main" 2>/dev/null || true
sleep 1

# Start the API server
echo -e "${GREEN}✅ Starting API server on http://localhost:8000${NC}"
echo ""
echo -e "${BLUE}📚 API Documentation: http://localhost:8000/api/docs${NC}"
echo -e "${BLUE}📊 Health Check: http://localhost:8000/api/health${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
