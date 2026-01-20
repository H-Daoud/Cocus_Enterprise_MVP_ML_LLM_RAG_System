#!/bin/bash
# ============================================================================
# Server Setup Script - HuggingFace API with Llama
# ============================================================================
# This script sets up secure secret storage for HuggingFace API
# Run this ONCE on your production server
# ============================================================================

set -e

echo "🔒 Setting up secure secret storage for HuggingFace API..."

# 1. Create secure directory
echo "📁 Creating /opt/secrets/mvp-rag..."
sudo mkdir -p /opt/secrets/mvp-rag

# 2. Set directory permissions (only root can access)
sudo chmod 700 /opt/secrets/mvp-rag

# 3. Create .env file with HuggingFace configuration
echo "📝 Creating .env file for HuggingFace Llama..."
sudo tee /opt/secrets/mvp-rag/.env > /dev/null << 'EOF'
# ============================================================================
# Production Secrets - HuggingFace API
# ============================================================================

# HuggingFace API Configuration
# Get your token from: https://huggingface.co/settings/tokens
OPENAI_API_KEY=hf_your_token_here
OPENAI_API_BASE=https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct
OPENAI_MODEL=meta-llama/Llama-3.2-3B-Instruct

# Application Settings
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO

# GCP Configuration (if using GCP)
# GCP_PROJECT_ID=your-project-id
# GCP_REGION=us-central1
EOF

# 4. Secure the file
sudo chmod 600 /opt/secrets/mvp-rag/.env
sudo chown root:root /opt/secrets/mvp-rag/.env

# 5. Verify
echo ""
echo "✅ Secret storage setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the secrets file:"
echo "   sudo nano /opt/secrets/mvp-rag/.env"
echo ""
echo "2. Replace 'hf_your_token_here' with your real HuggingFace token"
echo "   Get it from: https://huggingface.co/settings/tokens"
echo ""
echo "3. Verify permissions:"
echo "   ls -la /opt/secrets/mvp-rag/.env"
echo "   Should show: -rw------- 1 root root"
echo ""
echo "4. Run Docker Compose:"
echo "   sudo docker-compose up -d"
echo ""
echo "🤖 Using Llama 3.2-3B-Instruct via HuggingFace API"
echo ""
