"""
ui/sidebar.py — Upload & settings sidebar component
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st
from loguru import logger

import config
from core.document_loader import DocumentLoader
from core.ollama_client import OllamaClient


def render_sidebar() -> None:
    """Render the left sidebar with upload, model settings, and status."""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.divider()

        # ── Model Selection ───────────────────────────────────────────────────
        _render_model_selector()
        st.divider()

        # ── Document Upload ───────────────────────────────────────────────────
        _render_upload_section()
        st.divider()

        # ── Status ────────────────────────────────────────────────────────────
        _render_status_section()


def _render_model_selector() -> None:
    """Model selection and Ollama connection status."""
    st.markdown("### 🤖 Model")

    ollama = OllamaClient()
    is_connected = ollama.is_available()

    if is_connected:
        st.success("Ollama connected", icon="✅")
        models = ollama.list_models()
        if models:
            selected = st.selectbox(
                "Select model",
                options=models,
                index=models.index(st.session_state.ollama_model)
                if st.session_state.ollama_model in models
                else 0,
                key="model_selector",
            )
            if selected != st.session_state.ollama_model:
                st.session_state.ollama_model = selected
                # Rebuild pipeline with new model
                if st.session_state.rag_pipeline:
                    new_ollama = OllamaClient(model=selected)
                    st.session_state.rag_pipeline.update_model(new_ollama.get_llm())
                    st.success(f"Switched to {selected}")
        else:
            st.warning("No models found. Run: ollama pull llama3")
    else:
        st.error("Ollama not connected", icon="❌")
        st.code("ollama serve", language="bash")
        st.caption("Start Ollama to enable AI responses")


def _render_upload_section() -> None:
    """Document upload section with progress feedback."""
    st.markdown("### 📁 Upload Documents")

    ext_list = ", ".join(sorted(config.SUPPORTED_EXTENSIONS.keys()))
    st.caption(f"Supported: {ext_list}")

    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=[ext.lstrip(".") for ext in config.SUPPORTED_EXTENSIONS],
        label_visibility="collapsed",
    )

    if uploaded_files:
        if st.button("Index Documents", type="primary", use_container_width=True):
            _process_uploads(uploaded_files)


def _process_uploads(uploaded_files) -> None:
    """Process and index uploaded files."""
    if st.session_state.vector_store is None:
        st.error("Vector store not initialized. Please refresh.")
        return

    loader = DocumentLoader(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    progress = st.progress(0, text="Processing files...")
    total = len(uploaded_files)
    indexed = 0

    for i, uploaded_file in enumerate(uploaded_files):
        progress.progress((i) / total, text=f"Processing {uploaded_file.name}...")

        # Save to temp file
        suffix = Path(uploaded_file.name).suffix
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, mode="wb"
        ) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            # Check for duplicates
            import hashlib
            file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()

            if st.session_state.vector_store.source_exists(file_hash):
                st.info(f"Already indexed: {uploaded_file.name}")
                continue

            # Load and index
            chunks = loader.load_file(tmp_path)
            # Fix source name in metadata
            for chunk in chunks:
                chunk.metadata["source"] = uploaded_file.name

            st.session_state.vector_store.add_documents(chunks)
            st.session_state.documents_indexed.append(uploaded_file.name)
            indexed += 1
            st.success(f"Indexed: {uploaded_file.name} ({len(chunks)} chunks)")

        except Exception as e:
            st.error(f"Failed to index {uploaded_file.name}: {e}")
            logger.error(f"Upload error for {uploaded_file.name}: {e}")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    progress.progress(1.0, text="Done!")
    if indexed > 0:
        st.balloons()
        # Clear messages to start fresh after new documents
        st.session_state.messages = []


def _render_status_section() -> None:
    """Show current indexing statistics."""
    st.markdown("### 📊 Status")

    vs = st.session_state.vector_store
    if vs:
        count = vs.count()
        sources = vs.get_all_sources()
        st.metric("Total Chunks", count)
        st.metric("Documents Indexed", len(sources))

        if st.button("Clear All Documents", type="secondary", use_container_width=True):
            if st.confirm("This will delete all indexed documents. Are you sure?"):
                vs.reset()
                st.session_state.messages = []
                st.session_state.documents_indexed = []
                st.rerun()
    else:
        st.info("Initializing...")
