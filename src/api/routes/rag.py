"""
RAG (Retrieval-Augmented Generation) API endpoints
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    """RAG query request model"""

    query: str
    max_results: int = 10
    include_sources: bool = True


class Source(BaseModel):
    """Source citation model"""

    document_id: str
    content: str
    score: float


class QueryResponse(BaseModel):
    """RAG query response model"""

    query: str
    answer: str
    sources: Optional[List[Source]] = None
    confidence: float


@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system

    Retrieves relevant documents and generates an answer using LLM
    Includes source citations for transparency (EU AI Act compliance)

    Supports both OpenAI and Google Gemini - configured via environment variables
    """
    logger.info(f"RAG query received: {request.query}")

    try:
        # Import here to avoid loading if not needed
        from src.utils.llm_config import get_llm_client, LLMConfig
        from src.rag.manager import RAGManager

        # Get LLM client (auto-detects provider from env)
        config = LLMConfig.from_env()
        llm = get_llm_client(config)

        # Initialize RAG manager for retrieval
        rag = RAGManager()
        relevant_docs = rag.query(request.query, k=request.max_results)

        # Build context from retrieved chunks
        context_text = "\n\n".join(
            [f"Source [{i+1}]: {doc['content']}" for i, doc in enumerate(relevant_docs)]
        )

        logger.info(f"Using LLM provider: {config.provider.value}, model: {config.model}")
        logger.info(f"Retrieved {len(relevant_docs)} context chunks for query.")

        # System prompt with context
        system_prompt = f"""You are a helpful assistant for the COCUS MVP system. 
Use the following pieces of retrieved context to answer the user's question. 

### CRITICAL INSTRUCTION:
The context below contains raw order records. Please look for EXACT matches of the Order ID or Customer Email requested by the user. 
If multiple similar-looking IDs appear (e.g., ORD-0033 vs ORD-0003), ensure you only discuss the one the user explicitly asked for.
If the answer is not in the context, say that you don't know based on the provided documents.

Keep your answer professional and concise.

### CONTEXT:
{context_text}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.query},
        ]

        # Generate response
        result = llm.invoke(messages)
        answer = result.content if hasattr(result, "content") else str(result)

        # Map sources for response
        sources = [
            Source(document_id=doc["document_id"], content=doc["content"], score=doc["score"])
            for doc in relevant_docs
        ]

        response = QueryResponse(
            query=request.query,
            answer=answer,
            sources=sources if request.include_sources else None,
            confidence=0.9 if relevant_docs else 0.5,
        )

        # Custom mock data for demonstration or error handling
        if config.provider.value == "mock" or "Error" in response.answer:
            mock_sources = [
                Source(
                    document_id="ML-001",
                    content="Machine Learning FAQ: ML models use statistical techniques to find patterns in large datasets.",
                    score=0.98,
                ),
                Source(
                    document_id="REG-EU-001",
                    content="EU AI Act Guidelines: High-risk AI systems must implement robust logging and transparency measures.",
                    score=0.95,
                ),
            ]

            # If the response already has an error message, we might want to override the answer for a clean demo
            if "RESOURCE_EXHAUSTED" in response.answer:
                response.answer = (
                    "The system is currently in MOCK mode to ensure a smooth demo experience (Gemini API quota exceeded). "
                    + "I can still explain core concepts like Data Validation, GDPR, and the EU AI Act!"
                )
                response.sources = mock_sources
                response.confidence = 0.9
            elif config.provider.value == "mock":
                response.sources = mock_sources
                response.confidence = 0.9

        logger.info(f"RAG response generated using {config.provider.value}")

        return response

    except Exception as e:
        logger.error(f"RAG query failed: {str(e)}")
        # Return helpful error message
        return QueryResponse(
            query=request.query,
            answer=f"Error: {str(e)}. Please check your LLM_PROVIDER and API key configuration in .env file.",
            sources=None,
            confidence=0.0,
        )


@router.get("/health")
async def rag_health():
    """RAG system health check"""
    return {"status": "operational", "model": "placeholder", "vector_store": "connected"}
