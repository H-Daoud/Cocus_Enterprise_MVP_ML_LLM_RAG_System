
import os
import shutil
from typing import List, Optional, Dict
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.utils.logger import get_logger
from src.utils.llm_config import LLMConfig

logger = get_logger(__name__)

class RAGManager:
    """Manages the RAG pipeline: document ingestion, vector indexing, and retrieval"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RAGManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, persist_directory: str = "data/vectorstore"):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        load_dotenv()
        
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self._initialized = True
        
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

    def load_ndjson(self, file_path: str) -> List:
        """Parse orders from an NDJSON file and return as LangChain Documents"""
        import json
        from langchain_core.documents import Document
        
        logger.debug(f"Parsing orders from {file_path}...")
        
        if not os.path.exists(file_path):
            logger.error(f"File {file_path} not found!")
            return []

        documents = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        # Create a descriptive text representation for better RAG retrieval
                        order_id = data.get('order_id', 'N/A')
                        customer = data.get('customer_email', 'N/A')
                        
                        # Prepend keywords to help with exact string matching
                        text_content = f"ORDER_SEARCH_ID: {order_id}\nCUSTOMER_SEARCH_EMAIL: {customer}\n"
                        text_content += f"Order Details:\n"
                        text_content += f"Order ID: {order_id}\n"
                        text_content += f"Customer: {customer}\n"
                        text_content += f"Status: {data.get('status', 'N/A')}\n"
                        
                        qty = data.get('quantity', 0)
                        price = data.get('unit_price', 0)
                        text_content += f"Quantity: {qty}, Unit Price: {price}\n"
                        
                        shipping = data.get('shipping', {})
                        text_content += f"Shipping: {shipping.get('city', 'N/A')}, {shipping.get('country_code', 'N/A')}\n"
                        
                        tags = data.get('tags', [])
                        if isinstance(tags, str):
                            text_content += f"Tags: {tags}\n"
                        elif isinstance(tags, list):
                            text_content += f"Tags: {', '.join(tags)}\n"
                        
                        if data.get('coupon_code'):
                            text_content += f"Coupon: {data.get('coupon_code')}\n"
                        
                        if data.get('is_gift'):
                            text_content += f"Is Gift: {data.get('is_gift')}\n"

                        # Create LangChain Document
                        doc = Document(
                            page_content=text_content,
                            metadata={
                                "order_id": order_id,
                                "customer_email": customer,
                                "source": file_path,
                                "type": "order"
                            }
                        )
                        documents.append(doc)
                    except Exception as e:
                        logger.warning(f"Failed to parse line in {file_path}: {e}")
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return []
            
        return documents

    def index_folder(self, folder_path: str):
        """Scan a folder for all .ndjson files and index them"""
        logger.info(f"Scanning folder {folder_path} for data...")
        
        all_documents = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.ndjson'):
                    file_path = os.path.join(root, file)
                    docs = self.load_ndjson(file_path)
                    all_documents.extend(docs)
                    logger.info(f"Loaded {len(docs)} orders from {file}")

        if not all_documents:
            logger.warning("No data found to index.")
            return

        logger.info(f"Total orders to index: {len(all_documents)}")

        # Wipe existing store for a clean re-index
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
            os.makedirs(self.persist_directory)

        # Create and persist vector store
        self.vector_store = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        logger.info(f"Successfully indexed {len(all_documents)} orders to {self.persist_directory}")

    def get_vector_store(self):
        """Get or initialize the vector store"""
        if self.vector_store is None:
            if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
                logger.info("Loading existing vector store...")
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
            else:
                logger.warning("Vector store not found. Please run indexing first.")
        return self.vector_store

    def query(self, text: str, k: int = 10) -> List[Dict]:
        """Search for relevant document chunks using hybrid search (Vector + Exact Key matching)"""
        store = self.get_vector_store()
        if not store:
            return []
            
        # 1. Vector Search
        results = store.similarity_search_with_relevance_scores(text, k=k)
        
        sources = []
        found_ids = set()
        
        # 2. Exact Key Matching (Heuristic for IDs and Emails)
        # We also manually scan for exact matches if the text looks like an ID or email
        import re
        id_pattern = re.compile(r'ORD-\d{4}', re.IGNORECASE)
        email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        
        target_id = id_pattern.search(text)
        target_email = email_pattern.search(text)
        
        if target_id or target_email:
            logger.info("Specific ID or Email detected in query. Checking for exact matches...")
            # We can use the metadata filter if Chroma supports it, 
            # or just do a quick scan of documents if the dataset is small (it is 50 records)
            try:
                all_docs = store.get()
                for i, content in enumerate(all_docs['documents']):
                    doc_id = all_docs['metadatas'][i].get('order_id')
                    doc_email = all_docs['metadatas'][i].get('customer_email') # Assuming we added this to metadata
                    
                    # Case insensitive match for ID
                    is_id_match = target_id and doc_id and target_id.group().upper() == doc_id.upper()
                    # Case insensitive match for Email
                    is_email_match = target_email and doc_email and target_email.group().lower() == doc_email.lower()
                    
                    if is_id_match or is_email_match:
                        current_id = doc_id or f"email_{i}"
                        if current_id not in found_ids:
                            sources.append({
                                "content": content,
                                "document_id": all_docs['metadatas'][i].get('source', 'unknown'),
                                "score": 1.0 # Perfect match score
                            })
                            found_ids.add(current_id)
            except Exception as e:
                logger.error(f"Manual scan failed: {e}")

        # 3. Add Vector Results (avoiding duplicates)
        for doc, score in results:
            doc_id = doc.metadata.get("order_id")
            if doc_id not in found_ids:
                sources.append({
                    "content": doc.page_content,
                    "document_id": doc.metadata.get("source", "unknown"),
                    "score": float(score)
                })
                found_ids.add(doc_id)
                
        return sources[:k]
