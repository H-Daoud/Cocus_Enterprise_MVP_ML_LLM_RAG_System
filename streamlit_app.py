import json
import os

import pandas as pd
import streamlit as st

from src.rag.manager import RAGManager
from src.utils.llm_config import LLMConfig

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
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

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

                # 2. Setup LLM using LangChain (more reliable for Streamlit Cloud)
                from langchain_core.messages import HumanMessage, SystemMessage

                from src.utils.llm_config import get_llm_client

                llm = get_llm_client()

                # Format context for prompt
                context_str = "\n---\n".join([c["content"] for c in context])

                # Create messages
                messages = [
                    SystemMessage(
                        content="You are a professional COCUS RAG Agent. Use the provided context to answer questions about orders. Be concise and cite order IDs when relevant."
                    ),
                    HumanMessage(
                        content=f"Context:\n{context_str}\n\nQuestion: {prompt}\n\nProvide a clear answer and list any Order IDs you reference."
                    ),
                ]

                # Get response
                response = llm.invoke(messages)
                answer = response.content

                # Display Answer
                st.write(answer)

                # Display Context Sources
                if context:
                    with st.expander("📚 Retrieved Context"):
                        for i, ctx in enumerate(context[:3], 1):
                            st.markdown(f"**Source {i}** (Score: {ctx.get('score', 0):.2f})")
                            st.code(ctx["content"][:200] + "...")

            except Exception as e:
                answer = f"I'm sorry, I encountered an error: {str(e)}"
                st.error(answer)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
