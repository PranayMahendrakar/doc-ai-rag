"""
app.py — Streamlit entry point for doc-ai-rag
"""
import streamlit as st
from pathlib import Path

import config
from core.vector_store import VectorStoreManager
from core.rag_pipeline import RAGPipeline
from core.ollama_client import OllamaClient
from ui.sidebar import render_sidebar
from ui.chat import render_chat
from ui.document_manager import render_document_manager


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = None
    if "ollama_model" not in st.session_state:
        st.session_state.ollama_model = config.OLLAMA_MODEL
    if "documents_indexed" not in st.session_state:
        st.session_state.documents_indexed = []
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Chat"


def setup_components():
    """Initialize vector store and RAG pipeline if not already done."""
    if st.session_state.vector_store is None:
        with st.spinner("Initializing vector store..."):
            st.session_state.vector_store = VectorStoreManager(
                persist_dir=str(config.CHROMA_PERSIST_DIR),
                collection_name=config.CHROMA_COLLECTION_NAME,
                embedding_model=config.EMBEDDING_MODEL,
            )

    if st.session_state.rag_pipeline is None:
        with st.spinner("Setting up RAG pipeline..."):
            ollama = OllamaClient(
                base_url=config.OLLAMA_BASE_URL,
                model=st.session_state.ollama_model,
                temperature=config.OLLAMA_TEMPERATURE,
            )
            st.session_state.rag_pipeline = RAGPipeline(
                vector_store=st.session_state.vector_store,
                llm=ollama.get_llm(),
                top_k=config.TOP_K,
            )


def main():
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .stChatMessage {
            padding: 0.5rem 0;
        }
        .source-badge {
            background-color: #1e3a5f;
            color: #7eb6ff;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 0.75rem;
            font-family: monospace;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    initialize_session_state()

    # ── Sidebar ──────────────────────────────────────────────────────────────
    render_sidebar()

    # ── Setup core components ─────────────────────────────────────────────────
    try:
        setup_components()
    except Exception as e:
        st.error(
            f"Failed to initialize components: {e}\n\n"
            "Please ensure Ollama is running: `ollama serve`"
        )
        st.stop()

    # ── Main area ─────────────────────────────────────────────────────────────
    st.markdown(
        f'<h1 class="main-header">{config.APP_ICON} {config.APP_TITLE}</h1>',
        unsafe_allow_html=True,
    )
    st.caption(config.APP_DESCRIPTION)
    st.divider()

    tab_chat, tab_docs = st.tabs(["💬 Chat", "📁 Documents"])

    with tab_chat:
        render_chat(st.session_state.rag_pipeline)

    with tab_docs:
        render_document_manager(st.session_state.vector_store)


if __name__ == "__main__":
    main()
