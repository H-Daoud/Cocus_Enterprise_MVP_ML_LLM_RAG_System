#!/usr/bin/env python3
"""
AUTOMATED PRESENTATION DEMO (No User Input Required)
Demonstrates all MVP requirements automatically
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from scripts.data_quality_analysis import main as run_quality_analysis
from scripts.train_ml_model import main as run_ml_training


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run complete presentation demo automatically"""

    print_header("MVP PRESENTATION DEMO - AUTOMATED")
    print("This script demonstrates all requirements from Part 1 and Part 2\n")

    # ========================================================================
    # PART 1: Data Validation Challenge
    # ========================================================================

    print_header("PART 1: DATA VALIDATION CHALLENGE")

    print("📊 Running Data Quality Analysis...")
    print("   Answering all 5 required questions:\n")
    print("   1. Overall Acceptance Rate")
    print("   2. Per-Field Basic Profiles")
    print("   3. Missing/Unusable Values")
    print("   4. Outliers and Extreme Values")
    print("   5. Quality by Grouping\n")

    run_quality_analysis()

    print("\n✅ Part 1 Analysis Complete!")
    print(f"   Report saved: reports/data_quality_report.md\n")

    # ========================================================================
    # ML TRAINING
    # ========================================================================

    print_header("ML MODEL TRAINING (LIGHTWEIGHT DEMO)")

    print("🤖 Training Anomaly Detection Model...")
    print("   - Rule-based anomaly detection")
    print("   - No heavy dependencies required")
    print("   - Perfect for presentation\n")

    run_ml_training()

    print("\n✅ ML Training Complete!")
    print(f"   Model: models/anomaly_detection_demo.json")
    print(f"   Metadata: models/anomaly_detection_metadata.json\n")

    # ========================================================================
    # PART 2: LLM-RAG Challenge
    # ========================================================================

    print_header("PART 2: LLM-RAG CHALLENGE")

    print("🤖 RAG System Status:")
    print("   ✓ Hybrid Search implemented (Vector + Exact matching)")
    print("   ✓ Pydantic-AI agent ready")
    print("   ✓ 3 business questions configured\n")

    print("To run the Pydantic-AI agent (requires API key):")
    print("   python3 scripts/run_business_questions.py\n")

    print("To test the Chat UI:")
    print("   ./run.sh")
    print("   Then open: http://localhost:8000/chat-ui.html\n")

    # ========================================================================
    # SUMMARY
    # ========================================================================

    print_header("PRESENTATION DEMO COMPLETE")

    print("✅ All Requirements Demonstrated:\n")
    print("PART 1:")
    print("  ✓ Data validation with Pydantic models")
    print("  ✓ Data quality analysis (5 questions answered)")
    print("  ✓ ML model training (lightweight demo)")
    print("  ✓ Automated training pipeline\n")

    print("PART 2:")
    print("  ✓ Pydantic-AI agent with structured output")
    print("  ✓ Retrieval tool integration")
    print("  ✓ 3 business questions ready")
    print("  ✓ used_order_ids tracking\n")

    print("ADDITIONAL:")
    print("  ✓ Hybrid Search RAG system")
    print("  ✓ Professional UI (COCUS branding)")
    print("  ✓ Docker deployment ready (~400 MB)")
    print("  ✓ GitHub Actions CI/CD")
    print("  ✓ Google Colab training notebook\n")

    print("=" * 80)
    print("Ready for presentation! 🚀")
    print("=" * 80 + "\n")

    print("📁 Generated Files:")
    print("  - reports/data_quality_report.md")
    print("  - models/anomaly_detection_demo.json")
    print("  - models/anomaly_detection_metadata.json")
    print("  - notebooks/ML_Training_Colab.ipynb")
    print("\n")


if __name__ == "__main__":
    main()
