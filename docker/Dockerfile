# ============================================================================
# PRODUCTION DOCKERFILE - GCP Cloud Run Optimized
# ============================================================================
# Multi-stage build for minimal image size and security
# Target size: ~250-300 MB (optimized from 400 MB)
# ============================================================================

# ============================================================================
# STAGE 1: Builder - Install dependencies and compile
# ============================================================================
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies to a specific directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    rm -rf /root/.cache/pip

# ============================================================================
# STAGE 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.11-slim

# Metadata
LABEL maintainer="H. Daoud"
LABEL description="COCUS MVP - RAG System with ML Anomaly Detection"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code (as non-root user)
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser models/ ./models/
COPY --chown=appuser:appuser data/ ./data/
COPY --chown=appuser:appuser chat-ui.html ./
COPY --chown=appuser:appuser main.py ./

# Create necessary directories
RUN mkdir -p /app/logs /app/data/vectorstore && \
    chown -R appuser:appuser /app/logs /app/data

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command (can be overridden)
CMD ["python3", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
