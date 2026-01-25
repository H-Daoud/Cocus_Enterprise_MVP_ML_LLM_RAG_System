"""
LLM Provider Configuration
Supports OpenAI and Google Gemini
"""

import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class LLMProvider(str, Enum):
    """Supported LLM providers"""

    OPENAI = "openai"
    GEMINI = "gemini"
    MOCK = "mock"  # For testing without API keys


class LLMConfig(BaseModel):
    """LLM configuration"""

    provider: LLMProvider = LLMProvider.OPENAI  # Default to OpenAI (Hugging Face)
    api_key: Optional[str] = None
    model: str = "gemini-pro"
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """
        Load configuration from environment variables
        For development: uses .env file
        For production: falls back to enterprise secrets manager if available
        """
        provider_str = os.getenv("LLM_PROVIDER", "openai").lower()

        # Map provider string to enum
        provider_map = {
            "openai": LLMProvider.OPENAI,
            "gemini": LLMProvider.GEMINI,
            "google": LLMProvider.GEMINI,
            "mock": LLMProvider.MOCK,
        }
        provider = provider_map.get(provider_str, LLMProvider.OPENAI)

        # Try to get API key from environment first (for development)
        # Falls back to secrets manager if env var not found (for production)
        if provider == LLMProvider.OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                try:
                    from src.utils.secrets_manager import get_secrets_manager

                    api_key = get_secrets_manager().get_openai_key()
                except Exception as e:
                    from src.utils.logger import logger

                    logger.warning(f"Failed to retrieve OpenAI key from Secrets Manager: {e}")
                    pass
            model = os.getenv("OPENAI_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
        elif provider == LLMProvider.GEMINI:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                try:
                    from src.utils.secrets_manager import get_secrets_manager

                    api_key = get_secrets_manager().get_gemini_key()
                except Exception as e:
                    from src.utils.logger import logger

                    logger.warning(f"Failed to retrieve Gemini key from Secrets Manager: {e}")
                    pass
            model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        else:  # MOCK
            api_key = "mock-key-for-testing"
            model = "mock-model"

        return cls(
            provider=provider,
            api_key=api_key,
            model=model,
            base_url=os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_API_BASE"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000")),
        )

    def get_agent(self):
        """Get a Pydantic AI agent based on configuration"""
        from pydantic_ai import Agent
        from pydantic_ai.models.openai import OpenAIModel
        from typing import List
        from pydantic import BaseModel as PydanticBaseModel
        import os

        class OrderResponse(PydanticBaseModel):
            answer: str
            used_order_ids: List[str]

        if self.provider == LLMProvider.OPENAI:
            # pydantic-ai expects API key in environment variable
            if self.api_key:
                os.environ["OPENAI_API_KEY"] = self.api_key

            # For HuggingFace router, configure custom base_url via http_client
            if self.base_url:
                import httpx

                http_client = httpx.Client(base_url=self.base_url)
                model = OpenAIModel(self.model, http_client=http_client)
            else:
                model = OpenAIModel(self.model)

            return Agent(
                model=model,
                result_type=OrderResponse,
                system_prompt="You are a professional COCUS RAG Agent. Use the provided context to answer. List any Order IDs referenced.",
            )
        elif self.provider == LLMProvider.GEMINI:
            # Set API key for Gemini
            if self.api_key:
                os.environ["GEMINI_API_KEY"] = self.api_key

            try:
                from pydantic_ai.models.gemini import GeminiModel

                model = GeminiModel(self.model)
            except:
                # Fallback to OpenAI-compatible model
                if self.api_key:
                    os.environ["OPENAI_API_KEY"] = self.api_key
                model = OpenAIModel(self.model)

            return Agent(
                model=model,
                result_type=OrderResponse,
                system_prompt="You are a professional COCUS RAG Agent. Use context to answer. List Order IDs.",
            )
        else:

            class MockResult:
                class Data:
                    answer = (
                        "MOCK: This is a professional response about machine learning and orders."
                    )
                    used_order_ids = ["ORD-MOCK"]

                data = Data()

                def run_sync(self, *args, **kwargs):
                    return self

            return MockResult()


def get_llm_client(config: Optional[LLMConfig] = None):
    """
    Get LLM client based on configuration

    Args:
        config: LLM configuration (loads from env if not provided)

    Returns:
        LLM client instance
    """
    if config is None:
        config = LLMConfig.from_env()

    if config.provider == LLMProvider.OPENAI:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=config.api_key,
            model=config.model,
            base_url=config.base_url,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

    elif config.provider == LLMProvider.GEMINI:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            google_api_key=config.api_key,
            model=config.model,
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
        )

    else:  # MOCK
        # Return a professional mock client for testing
        class MockLLM:
            def invoke(self, messages):
                query = messages[-1].content if messages else ""
                responses = {
                    "machine learning": "Machine Learning (ML) is a subset of AI that focuses on building systems that learn from data to improve their performance over time without being explicitly programmed.",
                    "data validation": "Data validation is the process of ensuring data follows specific rules and formats before it is processed. In this project, we use Pydantic for robust, production-grade validation.",
                    "gdpr": "GDPR compliance ensures high data protection standards for personal data. This system implements automatic PII anonymization to help meet these requirements.",
                    "ai act": "The EU AI Act is a framework for regulating AI systems based on risk. This MVP includes automated audit logging to support compliance with transparency requirements.",
                }

                # Check for keywords in query
                response_text = "This is a professional mock response for testing. The system is currently in MOCK mode to preserve your API quota. Please ask about machine learning, data validation, or compliance for specific examples!"
                for key, val in responses.items():
                    if key in str(query).lower():
                        response_text = val
                        break

                class MockResponse:
                    def __init__(self, content):
                        self.content = content

                return MockResponse(response_text)

        return MockLLM()
