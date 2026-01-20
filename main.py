#!/usr/bin/env python3
"""
MASTER ORCHESTRATOR - Complete MVP Pipeline
Connects all components: Validation → Masking → EDA → ML → RAG

This is the single entry point for the entire system.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


class MVPOrchestrator:
    """
    Orchestrates the complete MVP pipeline following best practices:
    1. Data Validation (Pydantic)
    2. GDPR Masking
    3. Data Quality Analysis (Part 1)
    4. ML Training (Part 1)
    5. RAG Indexing (Part 2)
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.steps_completed = []
        self.steps_failed = []
    
    def print_header(self, title: str):
        """Print formatted section header"""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80 + "\n")
    
    def run_step(self, step_name: str, command: list, optional: bool = False) -> bool:
        """
        Run a pipeline step and track success/failure
        
        Args:
            step_name: Human-readable step name
            command: Command to execute
            optional: If True, failure won't stop the pipeline
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.print_header(f"STEP: {step_name}")
        
        print(f"🚀 Running: {' '.join(command)}\n")
        
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=False,
                text=True
            )
            
            self.steps_completed.append(step_name)
            print(f"\n✅ {step_name} - COMPLETE\n")
            return True
            
        except subprocess.CalledProcessError as e:
            self.steps_failed.append(step_name)
            print(f"\n❌ {step_name} - FAILED")
            
            if optional:
                print(f"⚠️  Continuing (optional step)...\n")
                return False
            else:
                print(f"🛑 Pipeline stopped due to critical failure\n")
                raise
    
    def run_pipeline(self, skip_optional: bool = False):
        """
        Execute the complete MVP pipeline
        
        Pipeline Flow:
        1. GDPR Data Processing (Validation + Masking)
        2. Data Quality Analysis (Part 1)
        3. ML Model Training (Part 1)
        4. RAG System Indexing (Part 2)
        5. (Optional) Business Questions Demo (Part 2)
        """
        
        print("="*80)
        print("MVP COMPLETE PIPELINE ORCHESTRATOR")
        print("="*80)
        print(f"\nStarted at: {self.start_time.isoformat()}")
        print(f"Skip optional steps: {skip_optional}\n")
        
        # ====================================================================
        # STEP 1: GDPR Data Processing
        # ====================================================================
        self.run_step(
            "1. GDPR Data Processing (Validation + Masking)",
            ["python3", "scripts/process_data_gdpr.py"]
        )
        
        # ====================================================================
        # STEP 2: Data Quality Analysis
        # ====================================================================
        self.run_step(
            "2. Data Quality Analysis (Part 1 - 5 Questions)",
            ["python3", "scripts/data_quality_analysis.py"]
        )
        
        # ====================================================================
        # STEP 3: ML Model Training
        # ====================================================================
        self.run_step(
            "3. ML Model Training (Isolation Forest → ONNX)",
            ["python3", "scripts/train_ml_model_real.py"]
        )
        
        # ====================================================================
        # STEP 4: RAG System Indexing
        # ====================================================================
        self.run_step(
            "4. RAG System Indexing (Vector Store)",
            ["./reindex.sh"],
            optional=True  # May fail if vectorstore already exists
        )
        
        # ====================================================================
        # STEP 5: Business Questions (Optional)
        # ====================================================================
        if not skip_optional:
            self.run_step(
                "5. Business Questions Demo (Part 2 - Pydantic-AI)",
                ["python3", "scripts/run_business_questions.py"],
                optional=True  # Requires API key
            )
        
        # ====================================================================
        # Pipeline Complete
        # ====================================================================
        self.print_summary()
    
    def print_summary(self):
        """Print pipeline execution summary"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        self.print_header("PIPELINE EXECUTION SUMMARY")
        
        print(f"⏱️  Duration: {duration:.1f} seconds\n")
        
        print(f"✅ Completed Steps ({len(self.steps_completed)}):")
        for i, step in enumerate(self.steps_completed, 1):
            print(f"  {i}. {step}")
        
        if self.steps_failed:
            print(f"\n❌ Failed Steps ({len(self.steps_failed)}):")
            for i, step in enumerate(self.steps_failed, 1):
                print(f"  {i}. {step}")
        
        print("\n" + "="*80)
        print("📁 Generated Artifacts:")
        print("="*80)
        print("""
  Part 1 (Data Validation & ML):
    - data/processed/orders_masked.ndjson    (GDPR-compliant data)
    - reports/data_quality_report.md         (5 questions answered)
    - models/anomaly_detection.onnx          (Production model)
    - models/anomaly_detection.pkl           (Sklearn model)
    - models/anomaly_detection_metadata.json (Model info)
  
  Part 2 (RAG System):
    - data/vectorstore/                      (ChromaDB index)
    - Chat UI: http://localhost:8000/chat-ui.html
        """)
        
        print("="*80)
        print("🎯 NEXT STEPS:")
        print("="*80)
        print("""
  For Presentation:
    1. Review: reports/data_quality_report.md
    2. Review: notebooks/Complete_ML_Pipeline_Andrew_Ng.ipynb
    3. Run: ./run.sh (Start RAG API server)
    4. Open: http://localhost:8000/chat-ui.html
  
  For Production:
    1. Deploy: Docker image to Google Cloud Run
    2. Setup: GitHub Actions CI/CD
    3. Monitor: Model performance and data quality
        """)
        
        if len(self.steps_failed) == 0:
            print("="*80)
            print("✅ ALL STEPS COMPLETED SUCCESSFULLY!")
            print("="*80 + "\n")
        else:
            print("="*80)
            print("⚠️  PIPELINE COMPLETED WITH WARNINGS")
            print("="*80 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MVP Complete Pipeline Orchestrator"
    )
    parser.add_argument(
        "--skip-optional",
        action="store_true",
        help="Skip optional steps (business questions demo)"
    )
    
    args = parser.parse_args()
    
    orchestrator = MVPOrchestrator()
    
    try:
        orchestrator.run_pipeline(skip_optional=args.skip_optional)
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
