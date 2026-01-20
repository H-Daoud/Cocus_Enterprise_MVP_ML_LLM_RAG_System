
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def test_connection():
    # Load environment variables from .env
    load_dotenv()
    
    provider = os.getenv("LLM_PROVIDER")
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL")
    
    print(f"Testing connectivity for provider: {provider}")
    print(f"Model: {model}")
    print(f"Base URL: {api_base}")
    
    if provider != "openai":
        print("Error: LLM_PROVIDER is not set to 'openai'")
        return

    try:
        # Initialize the LangChain client
        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            base_url=api_base,
            temperature=0
        )
        
        # Simple test query
        response = llm.invoke("Hello, who are you?")
        print("\n--- Response ---")
        print(response.content)
        print("----------------")
        print("\n✅ Connectivity test PASSED!")
        
    except Exception as e:
        print(f"\n❌ Connectivity test FAILED!")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
