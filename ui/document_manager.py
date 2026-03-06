"""
ui/document_manager.py — Document list and management UI
"""
from __future__ import annotations

import streamlit as st

from core.vector_store import VectorStoreManager


def render_document_manager(vector_store: VectorStoreManager | None) -> None:
    """Render the document management panel."""
    st.markdown("### 📁 Indexed Documents")

    if vector_store is None:
        st.info("Vector store initializing...")
        return

    sources = vector_store.get_all_sources()
    total_chunks = vector_store.count()

    if not sources:
        st.info(
            "No documents indexed yet. "
            "Upload files using the sidebar to get started.",
            icon="📂",
        )
        return

    # Summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", len(sources))
    with col2:
        st.metric("Total Chunks", total_chunks)

    st.divider()

    # Document table
    for doc in sources:
        with st.container(border=True):
            col_name, col_type, col_chunks, col_del = st.columns([4, 1, 1, 1])

            with col_name:
                icon = _get_file_icon(doc.get("file_type", ""))
                st.markdown(f"{icon} **{doc['source']}**")

            with col_type:
                file_type = doc.get("file_type", "?").upper()
                st.code(file_type, language=None)

            with col_chunks:
                st.caption(f"{doc.get('total_chunks', '?')} chunks")

            with col_del:
                if st.button("🗑️", key=f"del_{doc['source']}", help="Remove document"):
                    _delete_document(vector_store, doc["source"])


def _delete_document(vector_store: VectorStoreManager, source_name: str) -> None:
    """Delete a document from the vector store."""
    count = vector_store.delete_by_source(source_name)
    if count > 0:
        st.success(f"Removed {source_name} ({count} chunks deleted)")
        # Clear chat history since documents changed
        st.session_state.messages = []
        st.rerun()
    else:
        st.warning(f"Could not find {source_name} in the index")


def _get_file_icon(file_type: str) -> str:
    """Return an emoji icon for the file type."""
    icons = {
        "pdf": "📕",
        "docx": "📘",
        "doc": "📘",
        "csv": "📊",
        "excel": "📊",
        "txt": "📄",
        "markdown": "📝",
        "python": "🐍",
        "javascript": "🟨",
        "typescript": "🔷",
        "java": "☕",
        "json": "🔧",
        "yaml": "⚙️",
        "xml": "📋",
        "html": "🌐",
        "css": "🎨",
    }
    return icons.get(file_type.lower(), "📄")
