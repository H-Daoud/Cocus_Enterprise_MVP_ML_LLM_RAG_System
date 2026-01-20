#!/bin/bash

# ============================================================================
# Automated ML Training Pipeline
# ============================================================================
# Monitors data/raw folder and automatically trains ML model when new data arrives
# ============================================================================

set -e

DATA_DIR="data/raw"
MODEL_DIR="models"
LAST_TRAIN_FILE="$MODEL_DIR/.last_train_timestamp"

echo "🤖 Automated ML Training Pipeline"
echo "=================================="
echo ""

# Create models directory
mkdir -p "$MODEL_DIR"

# Check if new data exists
if [ ! -f "$DATA_DIR/orders_sample.ndjson" ]; then
    echo "❌ No data found in $DATA_DIR"
    exit 1
fi

# Check if we need to retrain
NEEDS_TRAINING=false

if [ ! -f "$LAST_TRAIN_FILE" ]; then
    echo "📌 No previous training detected. Training required."
    NEEDS_TRAINING=true
else
    # Check if data is newer than last training
    if [ "$DATA_DIR/orders_sample.ndjson" -nt "$LAST_TRAIN_FILE" ]; then
        echo "📌 New data detected. Retraining required."
        NEEDS_TRAINING=true
    else
        echo "✅ Model is up to date. No training needed."
    fi
fi

if [ "$NEEDS_TRAINING" = true ]; then
    echo ""
    echo "🚀 Starting ML training..."
    echo ""
    
    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Install required packages
    pip install -q scikit-learn onnx skl2onnx joblib
    
    # Run training
    python3 scripts/train_ml_model.py
    
    # Update timestamp
    date > "$LAST_TRAIN_FILE"
    
    echo ""
    echo "✅ Training complete! Model saved to $MODEL_DIR"
else
    echo ""
    echo "ℹ️  To force retraining, delete: $LAST_TRAIN_FILE"
fi

echo ""
echo "📊 Current models:"
ls -lh "$MODEL_DIR"/*.onnx "$MODEL_DIR"/*.pkl 2>/dev/null || echo "  No models found"
