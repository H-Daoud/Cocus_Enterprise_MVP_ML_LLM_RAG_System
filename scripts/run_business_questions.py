#!/usr/bin/env python3
"""
Pydantic-AI Agent for Order Analysis - Part 2 Requirement
Answers 3 core business questions with structured output
"""

import os
import sys
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.manager import RAGManager


# ============================================================================
# Output Schema (Part 2 Requirement)
# ============================================================================


class OrderAnalysisOutput(BaseModel):
    """Structured output for order analysis questions"""

    answer: str = Field(description="Natural language answer to the question")
    used_order_ids: List[str] = Field(description="Order IDs used as evidence")
    confidence: float = Field(description="Confidence score (0.0-1.0)", ge=0.0, le=1.0)


# ============================================================================
# Retrieval Tool (Part 2 Requirement)
# ============================================================================


class OrderRetrieval:
    """Retrieval tool for the pydantic-ai agent"""

    def __init__(self, rag_manager: RAGManager):
        self.rag_manager = rag_manager

    def search_orders(self, query: str, k: int = 5) -> List[dict]:
        """Search for relevant orders"""
        results = self.rag_manager.query(query, k=k)

        documents = []
        for doc in results:
            # Extract order_id from metadata or content
            order_id = doc.metadata.get("order_id", "UNKNOWN")
            if order_id == "UNKNOWN":
                # Try to extract from content
                import re

                match = re.search(r"ORDER_SEARCH_ID:\s*(ORD-\d+)", doc.page_content)
                if match:
                    order_id = match.group(1)

            documents.append({"order_id": order_id, "text": doc.page_content})

        return documents


# ============================================================================
# Pydantic-AI Agent (Part 2 Requirement)
# ============================================================================


def create_order_agent(rag_manager: RAGManager) -> Agent:
    """Create pydantic-ai agent with retrieval tool"""

    retrieval = OrderRetrieval(rag_manager)

    # System prompt (Part 2 Requirement)
    system_prompt = """You are an expert logistics data analyst.

CRITICAL INSTRUCTIONS:
1. Use ONLY the retrieved order documents as factual evidence
2. Do NOT invent order IDs or values not present in retrieved documents
3. ALWAYS fill in used_order_ids based on the retrieved documents you relied on
4. Provide specific, data-driven insights
5. Identify patterns, anomalies, and business rule violations

When analyzing orders, consider:
- Data quality issues (zero quantities, negative prices, invalid statuses)
- Business logic violations (refunded orders with high amounts, etc.)
- Coupon and tag usage patterns
- Suspicious combinations of fields
"""

    # Create agent with OpenAI-compatible endpoint
    agent = Agent(
        model="openai:" + os.getenv("OPENAI_MODEL", "meta-llama/Llama-3.2-3B-Instruct"),
        result_type=OrderAnalysisOutput,
        system_prompt=system_prompt,
    )

    # Register retrieval tool
    @agent.tool
    async def search_orders_tool(ctx: RunContext[None], query: str) -> str:
        """Search for relevant orders in the database"""
        docs = retrieval.search_orders(query, k=10)

        # Format results for the agent
        result = f"Found {len(docs)} relevant orders:\n\n"
        for doc in docs:
            result += f"Order ID: {doc['order_id']}\n{doc['text']}\n\n"

        return result

    return agent


# ============================================================================
# Business Questions (Part 2 Requirement)
# ============================================================================

BUSINESS_QUESTIONS = {
    "question_1": {
        "title": "Per-Order Explanation (ORD-0003)",
        "query": "Explain what is special or noteworthy about order ORD-0003 from a data quality or business perspective.",
    },
    "question_2": {
        "title": "Coupon and Tag Usage Patterns",
        "query": "Describe patterns of how coupon codes and tags like vip or promo are used across the accepted orders.",
    },
    "question_3": {
        "title": "Suspicious/Edge Cases",
        "query": "Based on the accepted orders, identify a few orders that look suspicious or edge-cases from a business rules perspective and explain why.",
    },
}


async def run_business_questions():
    """Run all 3 business questions and print results"""

    print("=" * 80)
    print("PYDANTIC-AI AGENT: BUSINESS QUESTIONS")
    print("=" * 80 + "\n")

    # Initialize RAG Manager
    print("📂 Initializing RAG system...")
    rag_manager = RAGManager()

    # Ensure index is built (Part 2 Requirement: 'Builds the index')
    if not rag_manager.get_vector_store():
        print("   ⚠️ Vector store not found. Building index now...")
        rag_manager.index_folder("data/raw")

    print("   ✓ RAG system ready\n")

    # Create agent
    print("🤖 Creating pydantic-ai agent...")
    agent = create_order_agent(rag_manager)
    print("   ✓ Agent ready\n")

    # Run each question
    for q_id, question in BUSINESS_QUESTIONS.items():
        print("=" * 80)
        print(f"QUESTION: {question['title']}")
        print("=" * 80)
        print(f"\n{question['query']}\n")

        try:
            # Run agent
            result = await agent.run(question["query"])

            # Print structured output
            print("ANSWER:")
            print(result.data.answer)
            print(f"\nUSED ORDER IDs: {', '.join(result.data.used_order_ids)}")
            print(f"CONFIDENCE: {result.data.confidence:.2f}")
            print("\n")

        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

    print("=" * 80)
    print("✅ ALL QUESTIONS COMPLETED")
    print("=" * 80)


def main():
    """Entry point"""
    import asyncio

    asyncio.run(run_business_questions())


if __name__ == "__main__":
    main()
