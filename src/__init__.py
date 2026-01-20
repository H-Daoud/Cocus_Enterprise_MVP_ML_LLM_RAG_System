"""
COCUS MVP ML/LLM RAG System - Enterprise Edition
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "COCUS Team"
__license__ = "MIT"

from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info(f"Initializing COCUS MVP System v{__version__}")
