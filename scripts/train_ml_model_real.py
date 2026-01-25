#!/usr/bin/env python3
"""
Real ML Model Training with ONNX Export
Requires: pip install scikit-learn onnx skl2onnx joblib
"""

import json
import sys
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.order import Order
from pydantic import ValidationError

# Import ML libraries
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    import joblib
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType
except ImportError as e:
    print(f"❌ Missing ML libraries. Please run:")
    print(f"   pip install scikit-learn onnx skl2onnx joblib")
    sys.exit(1)


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


def extract_features(orders: List[Order]):
    """Extract numerical features for ML training"""
    features = []
    feature_names = [
        "quantity",
        "unit_price",
        "total_amount",
        "has_coupon",
        "has_tags",
        "is_gift_flag",
        "status_encoded",
    ]

    status_map = {"pending": 0, "paid": 1, "shipped": 2, "cancelled": 3, "refunded": 4}

    for order in orders:
        total = order.quantity * order.unit_price

        feature_vector = [
            float(order.quantity),
            float(order.unit_price),
            float(total),
            1.0 if order.coupon_code else 0.0,
            1.0 if order.tags and len(order.tags) > 0 else 0.0,
            1.0 if order.is_gift else 0.0,
            float(status_map.get(order.status.lower(), 0)),
        ]
        features.append(feature_vector)

    return np.array(features), feature_names


def main():
    print("=" * 80)
    print("REAL ML MODEL TRAINING WITH ONNX EXPORT")
    print("=" * 80 + "\n")

    # 1. Load data
    print("📂 Loading validated orders...")
    orders = load_validated_orders("data/raw/orders_sample.ndjson")
    print(f"   ✓ Loaded {len(orders)} validated orders\n")

    # 2. Extract features
    print("🔧 Extracting features...")
    X, feature_names = extract_features(orders)
    print(f"   ✓ Extracted {X.shape[1]} features from {X.shape[0]} samples")
    print(f"   Features: {', '.join(feature_names)}\n")

    # 3. Train model
    print("🤖 Training Isolation Forest model...")
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", IsolationForest(contamination=0.1, random_state=42, n_estimators=100)),
        ]
    )

    pipeline.fit(X)

    # Predict anomalies
    predictions = pipeline.predict(X)
    anomaly_count = np.sum(predictions == -1)

    print(f"   ✓ Model trained on {X.shape[0]} samples")
    print(f"   ✓ Detected {anomaly_count} anomalies ({anomaly_count/X.shape[0]*100:.1f}%)\n")

    # 4. Export to ONNX
    print("📦 Exporting to ONNX format...")

    initial_type = [("float_input", FloatTensorType([None, len(feature_names)]))]
    onnx_model = convert_sklearn(
        pipeline, initial_types=initial_type, target_opset={"": 12, "ai.onnx.ml": 3}
    )

    # Save ONNX model
    Path("models").mkdir(exist_ok=True)
    onnx_path = "models/anomaly_detection.onnx"
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    print(f"   ✓ ONNX model saved: {onnx_path}")

    # 5. Save sklearn model
    sklearn_path = "models/anomaly_detection.pkl"
    joblib.dump({"model": pipeline, "trained_at": datetime.now().isoformat()}, sklearn_path)

    print(f"   ✓ Sklearn model saved: {sklearn_path}")

    # 6. Save metadata
    metadata = {
        "model_type": "IsolationForest",
        "feature_names": feature_names,
        "trained_at": datetime.now().isoformat(),
        "num_features": len(feature_names),
        "num_samples": X.shape[0],
        "contamination": 0.1,
        "anomalies_detected": int(anomaly_count),
        "anomaly_rate": f"{anomaly_count/X.shape[0]*100:.1f}%",
    }

    metadata_path = "models/anomaly_detection_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"   ✓ Metadata saved: {metadata_path}\n")

    # 7. Summary
    print("=" * 80)
    print("✅ TRAINING COMPLETE!")
    print("=" * 80)
    print(f"\nModel Summary:")
    print(f"  - Type: Isolation Forest")
    print(f"  - Training Data: {X.shape[0]} validated orders")
    print(f"  - Anomalies Found: {anomaly_count} ({anomaly_count/X.shape[0]*100:.1f}%)")
    print(f"  - ONNX Model: {onnx_path}")
    print(f"  - Sklearn Model: {sklearn_path}")
    print(f"  - Metadata: {metadata_path}\n")


if __name__ == "__main__":
    main()
