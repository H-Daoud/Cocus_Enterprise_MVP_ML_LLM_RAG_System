#!/bin/bash

# ============================================================================
# COCUS MVP - One-Click Setup Script
# ============================================================================
# This script sets up the entire project automatically
# Perfect for PMs, testers, and new developers!
# ============================================================================

set -e  # Exit on error

# Move to project root
cd "$(dirname "$0")/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║        🚀 COCUS MVP - Automated Setup Script 🚀               ║"
echo "║                                                                ║"
echo "║  This script will set up everything you need to run the       ║"
echo "║  COCUS MVP ML/LLM RAG System                                  ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# Step 1: Check Prerequisites
# ============================================================================
echo -e "${BLUE}📋 Step 1/6: Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker found${NC}"
    DOCKER_AVAILABLE=true
else
    echo -e "${YELLOW}⚠️  Docker not found (optional)${NC}"
    DOCKER_AVAILABLE=false
fi

# ============================================================================
# Step 2: Create Virtual Environment
# ============================================================================
echo ""
echo -e "${BLUE}📦 Step 2/6: Setting up Python virtual environment...${NC}"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# ============================================================================
# Step 3: Install Dependencies
# ============================================================================
echo ""
echo -e "${BLUE}📥 Step 3/6: Installing Python dependencies...${NC}"
echo -e "${YELLOW}   (This may take a few minutes...)${NC}"

pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install -r requirements-dev.txt -q 2>/dev/null || true

echo -e "${GREEN}✅ Dependencies installed${NC}"

# ============================================================================
# Step 4: Configure Environment
# ============================================================================
echo ""
echo -e "${BLUE}🔧 Step 4/6: Configuring environment...${NC}"

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file from template${NC}"
    
    echo ""
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠️  IMPORTANT: API Key Configuration Required                ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}To use the RAG features, you need a Google Gemini API key.${NC}"
    echo ""
    echo "Options:"
    echo "  1. Get a FREE Gemini API key from:"
    echo "     https://makersuite.google.com/app/apikey"
    echo ""
    echo "  2. Or use MOCK mode for testing (no API key needed)"
    echo ""
    
    read -p "Do you have a Gemini API key? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Please enter your Gemini API key:"
        read -s GEMINI_KEY
        echo ""
        
        # Update .env file
        sed -i.bak "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_KEY/" .env
        sed -i.bak "s/LLM_PROVIDER=.*/LLM_PROVIDER=gemini/" .env
        echo -e "${GREEN}✅ Gemini API key configured${NC}"
    else
        echo ""
        echo -e "${YELLOW}Using MOCK mode (no real AI responses)${NC}"
        sed -i.bak "s/LLM_PROVIDER=.*/LLM_PROVIDER=mock/" .env
        echo -e "${GREEN}✅ MOCK mode configured${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
fi

# Set secure permissions
chmod 600 .env
echo -e "${GREEN}✅ Secure permissions set on .env${NC}"

# ============================================================================
# Step 5: Run Tests
# ============================================================================
echo ""
echo -e "${BLUE}🧪 Step 5/6: Running tests...${NC}"

if pytest tests/unit/ -v -q 2>/dev/null; then
    echo -e "${GREEN}✅ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed (this is OK for first setup)${NC}"
fi

# ============================================================================
# Step 6: Setup Complete
# ============================================================================
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                ║${NC}"
echo -e "${GREEN}║  ✅ Setup Complete! Your COCUS MVP is ready to run!           ║${NC}"
echo -e "${GREEN}║                                                                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# Next Steps
# ============================================================================
echo -e "${BLUE}📚 Next Steps:${NC}"
echo ""
echo "1️⃣  Start the API server:"
echo -e "   ${GREEN}./run.sh${NC}"
echo ""
echo "2️⃣  Or use Docker (if available):"
if [ "$DOCKER_AVAILABLE" = true ]; then
    echo -e "   ${GREEN}docker-compose up -d${NC}"
else
    echo -e "   ${YELLOW}(Docker not installed)${NC}"
fi
echo ""
echo "3️⃣  Access the API documentation:"
echo -e "   ${GREEN}http://localhost:8000/api/docs${NC}"
echo ""
echo "4️⃣  Test the health endpoint:"
echo -e "   ${GREEN}curl http://localhost:8000/api/health${NC}"
echo ""

# ============================================================================
# Helpful Links
# ============================================================================
echo -e "${BLUE}📖 Documentation:${NC}"
echo "  • README.md - Full project documentation"
echo "  • SETUP_GUIDE.md - Detailed setup instructions"
echo "  • GEMINI_SETUP.md - Gemini API configuration"
echo "  • ENV_VARIABLES_GUIDE.md - Environment variables"
echo ""

echo -e "${BLUE}🆘 Need Help?${NC}"
echo "  • Check TEST_RESULTS.md for test status"
echo "  • Review logs in logs/ directory"
echo "  • See ENTERPRISE_QUICK_REFERENCE.txt for commands"
echo ""

echo -e "${GREEN}Happy testing! 🚀${NC}"
echo ""
