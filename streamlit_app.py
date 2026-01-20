import streamlit as st
import os
import json
from src.rag.manager import RAGManager
from src.utils.llm_config import LLMConfig
import pandas as pd

# Load secrets from Streamlit for Cloud deployment
if hasattr(st, "secrets"):
    for key, value in st.secrets.items():
        if isinstance(value, str):
            os.environ[key] = value

# Page config
st.set_page_config(
    page_title="COCUS RAG Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: #ffffff;
    }
    .chat-message.bot {
        background-color: #e9ecef;
        color: #212529;
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .content {
      width: 80%;
    }
    .stButton>button {
        background-color: #005691;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_manager" not in st.session_state:
    # Initialize RAG Manager
    with st.spinner("Initializing Enterprise Knowledge Base..."):
        manager = RAGManager()
        # Index data if vector store doesn't exist or is empty
        if not os.path.exists("data/vectorstore") or not os.listdir("data/vectorstore"):
            manager.index_folder("data/raw")
        st.session_state.rag_manager = manager

# Sidebar
with st.sidebar:
    st.image("https://www.cocus.com/wp-content/themes/cocus/img/logo.svg", width=150)
    st.title("Settings")
    st.info("Ask questions about enterprise orders, coupons, and suspicious activities.")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.write("© 2026 H. Daoud")

# Main Header
st.title("🚀 COCUS Enterprise RAG Agent")
st.markdown("---")

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("What would you like to know about the orders?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Retrieving intelligence..."):
            # Use RAG Manager to query
            try:
                # 1. Retrieve Context
                context = st.session_state.rag_manager.query(prompt)
                
                # 2. Setup LLM and Query
                config = LLMConfig()
                agent = config.get_agent()
                
                # Format context for prompt
                context_str = "\n---\n".join([c["content"] for c in context])
                full_prompt = f"Use the following order context to answer the user question. Context:\n{context_str}\n\nQuestion: {prompt}"
                
                # Get response
                response = agent.run_sync(full_prompt)
                answer = response.data.answer
                citations = response.data.used_order_ids
                
                # Display Answer
                st.write(answer)
                
                # Display Citations
                if citations:
                    with st.expander("📚 Source Citations"):
                        for cid in citations:
                            st.code(f"Order: {cid}")
                
            except Exception as e:
                answer = f"I'm sorry, I encountered an error: {str(e)}"
                st.error(answer)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
