"""
Data splitter implementing Andrew Ng's ML methodology
Train, Train-Dev, Dev, Test split strategy
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict
from sklearn.model_selection import train_test_split
import json
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataSplitter:
    """
    Implements Andrew Ng's dataset splitting methodology:
    - Train set: For model training (70-80%)
    - Train-dev set: For detecting overfitting (from same distribution as train)
    - Dev set: For hyperparameter tuning (from target distribution)
    - Test set: For final unbiased evaluation
    """
    
    def __init__(
        self,
        train_ratio: float = 0.70,
        train_dev_ratio: float = 0.10,
        dev_ratio: float = 0.10,
        test_ratio: float = 0.10,
        random_state: int = 42
    ):
        """
        Initialize data splitter with ratios
        
        Args:
            train_ratio: Proportion for training set
            train_dev_ratio: Proportion for train-dev set (overfitting detection)
            dev_ratio: Proportion for development set (hyperparameter tuning)
            test_ratio: Proportion for test set (final evaluation)
            random_state: Random seed for reproducibility
        """
        # Validate ratios sum to 1.0
        total = train_ratio + train_dev_ratio + dev_ratio + test_ratio
        if not np.isclose(total, 1.0):
            raise ValueError(f"Ratios must sum to 1.0, got {total}")
        
        self.train_ratio = train_ratio
        self.train_dev_ratio = train_dev_ratio
        self.dev_ratio = dev_ratio
        self.test_ratio = test_ratio
        self.random_state = random_state
        
        logger.info(f"DataSplitter initialized with ratios: "
                   f"Train={train_ratio}, Train-Dev={train_dev_ratio}, "
                   f"Dev={dev_ratio}, Test={test_ratio}")
    
    def split(
        self,
        data: pd.DataFrame,
        stratify_column: str = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Split data into train, train-dev, dev, and test sets
        
        Args:
            data: Input DataFrame
            stratify_column: Column to use for stratified splitting
        
        Returns:
            Dictionary with keys: 'train', 'train_dev', 'dev', 'test'
        """
        logger.info(f"Splitting {len(data)} samples into train/train-dev/dev/test sets")
        
        # First split: separate train+train_dev from dev+test
        train_traindev_size = self.train_ratio + self.train_dev_ratio
        
        stratify = data[stratify_column] if stratify_column else None
        
        train_traindev, dev_test = train_test_split(
            data,
            train_size=train_traindev_size,
            random_state=self.random_state,
            stratify=stratify
        )
        
        # Second split: separate train from train-dev
        train_size_adjusted = self.train_ratio / train_traindev_size
        
        stratify_train = train_traindev[stratify_column] if stratify_column else None
        
        train, train_dev = train_test_split(
            train_traindev,
            train_size=train_size_adjusted,
            random_state=self.random_state,
            stratify=stratify_train
        )
        
        # Third split: separate dev from test
        dev_size_adjusted = self.dev_ratio / (self.dev_ratio + self.test_ratio)
        
        stratify_dev = dev_test[stratify_column] if stratify_column else None
        
        dev, test = train_test_split(
            dev_test,
            train_size=dev_size_adjusted,
            random_state=self.random_state,
            stratify=stratify_dev
        )
        
        splits = {
            'train': train,
            'train_dev': train_dev,
            'dev': dev,
            'test': test
        }
        
        # Log split statistics
        logger.info("Dataset split completed:")
        for split_name, split_data in splits.items():
            logger.info(f"  {split_name}: {len(split_data)} samples "
                       f"({len(split_data)/len(data)*100:.1f}%)")
        
        return splits
    
    def save_splits(
        self,
        splits: Dict[str, pd.DataFrame],
        output_dir: Path,
        file_format: str = 'ndjson'
    ) -> Dict[str, Path]:
        """
        Save splits to disk
        
        Args:
            splits: Dictionary of split DataFrames
            output_dir: Output directory
            file_format: File format ('ndjson', 'csv', 'parquet')
        
        Returns:
            Dictionary mapping split names to file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_paths = {}
        
        for split_name, split_data in splits.items():
            if file_format == 'ndjson':
                file_path = output_dir / f"{split_name}.ndjson"
                split_data.to_json(file_path, orient='records', lines=True)
            elif file_format == 'csv':
                file_path = output_dir / f"{split_name}.csv"
                split_data.to_csv(file_path, index=False)
            elif file_format == 'parquet':
                file_path = output_dir / f"{split_name}.parquet"
                split_data.to_parquet(file_path, index=False)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
            
            file_paths[split_name] = file_path
            logger.info(f"Saved {split_name} split to {file_path}")
        
        # Save metadata
        metadata = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_samples': sum(len(df) for df in splits.values()),
            'splits': {
                name: {
                    'count': len(df),
                    'percentage': len(df) / sum(len(d) for d in splits.values()) * 100,
                    'file': str(path)
                }
                for name, (df, path) in zip(splits.keys(), 
                                            zip(splits.values(), file_paths.values()))
            },
            'ratios': {
                'train': self.train_ratio,
                'train_dev': self.train_dev_ratio,
                'dev': self.dev_ratio,
                'test': self.test_ratio
            },
            'random_state': self.random_state
        }
        
        metadata_path = output_dir / 'split_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved split metadata to {metadata_path}")
        
        return file_paths
    
    @staticmethod
    def load_split(file_path: Path, file_format: str = 'ndjson') -> pd.DataFrame:
        """
        Load a split from disk
        
        Args:
            file_path: Path to split file
            file_format: File format
        
        Returns:
            DataFrame containing the split
        """
        file_path = Path(file_path)
        
        if file_format == 'ndjson':
            return pd.read_json(file_path, lines=True)
        elif file_format == 'csv':
            return pd.read_csv(file_path)
        elif file_format == 'parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")


def analyze_split_distribution(splits: Dict[str, pd.DataFrame], column: str) -> Dict:
    """
    Analyze distribution of a column across splits
    Useful for detecting data mismatch between train-dev and dev sets
    
    Args:
        splits: Dictionary of split DataFrames
        column: Column to analyze
    
    Returns:
        Dictionary with distribution statistics
    """
    distributions = {}
    
    for split_name, split_data in splits.items():
        if column in split_data.columns:
            value_counts = split_data[column].value_counts(normalize=True)
            distributions[split_name] = value_counts.to_dict()
    
    return distributions
