"""
Script to split dataset using Andrew Ng methodology
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ml.preprocessing.data_splitter import DataSplitter
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Split dataset using Andrew Ng's methodology (Train/Train-Dev/Dev/Test)"
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input data file (NDJSON, CSV, or Parquet)"
    )
    parser.add_argument(
        "--output-dir", type=str, default="data/processed", help="Output directory for splits"
    )
    parser.add_argument(
        "--train-ratio", type=float, default=0.70, help="Training set ratio (default: 0.70)"
    )
    parser.add_argument(
        "--train-dev-ratio",
        type=float,
        default=0.10,
        help="Train-dev set ratio for overfitting detection (default: 0.10)",
    )
    parser.add_argument(
        "--dev-ratio",
        type=float,
        default=0.10,
        help="Development set ratio for hyperparameter tuning (default: 0.10)",
    )
    parser.add_argument(
        "--test-ratio",
        type=float,
        default=0.10,
        help="Test set ratio for final evaluation (default: 0.10)",
    )
    parser.add_argument(
        "--stratify", type=str, default=None, help="Column name for stratified splitting"
    )
    parser.add_argument(
        "--random-state", type=int, default=42, help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["ndjson", "csv", "parquet"],
        default="ndjson",
        help="Output file format (default: ndjson)",
    )

    args = parser.parse_args()

    # Load data
    input_path = Path(args.input)
    logger.info(f"Loading data from {input_path}")

    if input_path.suffix == ".ndjson":
        data = pd.read_json(input_path, lines=True)
    elif input_path.suffix == ".csv":
        data = pd.read_csv(input_path)
    elif input_path.suffix == ".parquet":
        data = pd.read_parquet(input_path)
    else:
        raise ValueError(f"Unsupported file format: {input_path.suffix}")

    logger.info(f"Loaded {len(data)} samples")

    # Initialize splitter
    splitter = DataSplitter(
        train_ratio=args.train_ratio,
        train_dev_ratio=args.train_dev_ratio,
        dev_ratio=args.dev_ratio,
        test_ratio=args.test_ratio,
        random_state=args.random_state,
    )

    # Split data
    splits = splitter.split(data, stratify_column=args.stratify)

    # Save splits
    output_dir = Path(args.output_dir)
    file_paths = splitter.save_splits(splits, output_dir, file_format=args.format)

    logger.info("Dataset splitting completed successfully!")
    logger.info(f"Splits saved to {output_dir}")
    logger.info("\nAndrew Ng Methodology:")
    logger.info("  - Train: For model training")
    logger.info("  - Train-Dev: For detecting overfitting (bias detection)")
    logger.info("  - Dev: For hyperparameter tuning (variance analysis)")
    logger.info("  - Test: For final unbiased evaluation")

    # Print file paths
    logger.info("\nGenerated files:")
    for split_name, file_path in file_paths.items():
        logger.info(f"  {split_name}: {file_path}")


if __name__ == "__main__":
    main()
