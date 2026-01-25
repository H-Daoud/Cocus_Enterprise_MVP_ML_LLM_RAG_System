import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.manager import RAGManager
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    raw_data_dir = "data/raw"
    vector_dir = "data/vectorstore"

    if not os.path.exists(raw_data_dir):
        logger.error(f"Raw data directory {raw_data_dir} not found!")
        return

    # Initialize RAG Manager
    rag = RAGManager(persist_directory=vector_dir)

    # Process and index
    logger.info(f"Starting bulk indexing for all orders in {raw_data_dir}...")
    rag.index_folder(raw_data_dir)
    logger.info("Indexing complete!")


if __name__ == "__main__":
    main()
