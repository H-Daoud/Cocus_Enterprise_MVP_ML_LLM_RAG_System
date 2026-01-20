#!/bin/bash

# COCUS MVP - Quick Start Script
# This script helps you get started quickly

set -e  # Exit on error

# Move to project root
cd "$(dirname "$0")/.."

echo "🚀 COCUS MVP - Quick Start Setup"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install requirements
echo "📥 Installing Python dependencies..."
echo "   (This may take a few minutes...)"
pip install -r requirements.txt -q

echo ""
echo "✅ Python dependencies installed!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys if needed"
    echo ""
fi

# Check Docker
echo "🐳 Checking Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    if docker ps &> /dev/null; then
        echo "✅ Docker is running"
    else
        echo "⚠️  Docker is installed but not running"
        echo "   Please start Docker Desktop"
    fi
else
    echo "❌ Docker is not installed"
    echo "   Install from: https://www.docker.com/products/docker-desktop/"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Configure API Keys (optional):"
echo "   nano .env"
echo "   # Add OPENAI_API_KEY if you want RAG features"
echo ""
echo "2. Start with Docker (recommended):"
echo "   docker-compose up -d"
echo ""
echo "3. OR run API locally:"
echo "   source venv/bin/activate"
echo "   uvicorn src.api.main:app --reload"
echo ""
echo "4. Test the API:"
echo "   curl http://localhost:8000/api/health"
echo ""
echo "5. View API documentation:"
echo "   open http://localhost:8000/api/docs"
echo ""
echo "📚 For detailed instructions, see SETUP_GUIDE.md"
echo ""
