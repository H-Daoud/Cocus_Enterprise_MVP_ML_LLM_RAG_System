#!/bin/bash

# ============================================================================
# Docker Build Script - Optimized Builds
# ============================================================================

set -e

echo "🐳 Docker Image Build Options"
echo ""
echo "1. OPTIMIZED (Recommended) - ~400-500 MB"
echo "   - Multi-stage Alpine build"
echo "   - Fast startup, embedding model included"
echo ""
echo "2. ULTRA-SLIM - ~200-300 MB"
echo "   - Minimal dependencies"
echo "   - Slower first startup (downloads model)"
echo ""

read -p "Choose build type (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🔨 Building OPTIMIZED image..."
    docker build -t mvp-rag-system:optimized .
    IMAGE_TAG="optimized"
elif [ "$choice" = "2" ]; then
    echo ""
    echo "🔨 Building ULTRA-SLIM image..."
    docker build -f Dockerfile.slim -t mvp-rag-system:slim .
    IMAGE_TAG="slim"
else
    echo "Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "✅ Build complete!"
echo ""
echo "📦 Image Size Comparison:"
docker images mvp-rag-system --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo "To run locally:"
echo "  docker run -p 8000:8000 --env-file .env mvp-rag-system:$IMAGE_TAG"
echo ""
echo "To deploy to Google Cloud:"
echo "  gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mvp-rag-system:$IMAGE_TAG"
echo ""
