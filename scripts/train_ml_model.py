#!/usr/bin/env python3
"""
Lightweight ML Training Demo (No Heavy Dependencies Required)
Perfect for presentations - demonstrates the concept without sklearn/onnx installation
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from pydantic import ValidationError

from src.models.order import Order


def load_validated_orders(file_path: str) -> List[Order]:
    """Load only validated orders from NDJSON"""
    accepted = []

    with open(file_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                order = Order(**data)
                accepted.append(order)
            except (json.JSONDecodeError, ValidationError):
                continue

    return accepted


def analyze_for_anomalies(orders: List[Order]) -> dict:
    """Simple rule-based anomaly detection (no ML needed)"""
    anomalies = []

    for i, order in enumerate(orders):
        reasons = []

        # Check for suspicious patterns
        total = order.quantity * order.unit_price

        if order.quantity == 0:
            reasons.append("Zero quantity")
        if order.unit_price <= 0:
            reasons.append("Invalid price")
        if total > 500:
            reasons.append("Unusually high total")
        if order.quantity >= 10:
            reasons.append("Extreme quantity")
        if order.status.lower() == "refunded" and total > 100:
            reasons.append("High-value refund")

        if reasons:
            anomalies.append({"order_id": order.order_id, "index": i, "reasons": reasons})

    return {
        "total_orders": len(orders),
        "anomalies_detected": len(anomalies),
        "anomaly_rate": f"{len(anomalies)/len(orders)*100:.1f}%",
        "anomalies": anomalies,
    }


def create_mock_onnx_model(output_path: str, metadata: dict):
    """Create a mock ONNX model file for demonstration"""
    # Create a minimal valid ONNX-like structure
    mock_model = {
        "model_type": "IsolationForest",
        "framework": "scikit-learn",
        "format": "ONNX",
        "version": "1.0",
        "metadata": metadata,
        "note": "This is a demonstration model. For production, train using Google Colab or cloud resources.",
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Save as JSON (mock ONNX)
    with open(output_path.replace(".onnx", "_demo.json"), "w") as f:
        json.dump(mock_model, f, indent=2)

    # Save metadata
    metadata_path = output_path.replace(".onnx", "_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return metadata_path


def main():
    print("=" * 80)
    print("ML MODEL TRAINING DEMO (Lightweight - No Heavy Dependencies)")
    print("=" * 80 + "\n")

    # 1. Load validated data
    print("📂 Loading validated orders...")
    orders = load_validated_orders("data/raw/orders_sample.ndjson")
    print(f"   ✓ Loaded {len(orders)} validated orders\n")

    # 2. Analyze for anomalies
    print("🔍 Analyzing for anomalies using rule-based detection...")
    analysis = analyze_for_anomalies(orders)

    print(f"   ✓ Total Orders: {analysis['total_orders']}")
    print(f"   ✓ Anomalies Detected: {analysis['anomalies_detected']}")
    print(f"   ✓ Anomaly Rate: {analysis['anomaly_rate']}\n")

    if analysis["anomalies"]:
        print("   Detected Anomalies:")
        for anomaly in analysis["anomalies"][:5]:  # Show first 5
            print(f"     - {anomaly['order_id']}: {', '.join(anomaly['reasons'])}")
        if len(analysis["anomalies"]) > 5:
            print(f"     ... and {len(analysis['anomalies']) - 5} more")
        print()

    # 3. Create model metadata
    print("📦 Creating model artifacts...")
    metadata = {
        "model_type": "Rule-Based Anomaly Detection",
        "trained_at": datetime.now().isoformat(),
        "num_samples": len(orders),
        "anomalies_detected": analysis["anomalies_detected"],
        "anomaly_rate": analysis["anomaly_rate"],
        "features": ["quantity", "unit_price", "total_amount", "status", "business_rules"],
        "note": "For production ML model, use Google Colab notebook: notebooks/ML_Training_Colab.ipynb",
    }

    # 4. Save model
    model_path = "models/anomaly_detection.onnx"
    metadata_path = create_mock_onnx_model(model_path, metadata)

    print(f"   ✓ Model metadata saved: {metadata_path}")
    print(f"   ✓ Demo model saved: models/anomaly_detection_demo.json\n")

    # 5. Summary
    print("=" * 80)
    print("✅ TRAINING DEMO COMPLETE!")
    print("=" * 80)
    print(f"\nModel Summary:")
    print(f"  - Approach: Rule-based anomaly detection")
    print(f"  - Training Data: {len(orders)} validated orders")
    print(f"  - Anomalies Found: {analysis['anomalies_detected']} ({analysis['anomaly_rate']})")
    print(f"  - Model Files: models/anomaly_detection_demo.json")
    print(f"\n💡 For production ML model:")
    print(f"  - Use: notebooks/ML_Training_Colab.ipynb")
    print(f"  - Or: GitHub Actions automated training workflow")
    print(f"  - Zero local installation required!\n")


if __name__ == "__main__":
    main()
