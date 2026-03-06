"""
ui/chat.py — Conversational chat interface for doc-ai-rag
"""
from __future__ import annotations

import streamlit as st

from core.rag_pipeline import RAGPipeline


def render_chat(pipeline: RAGPipeline | None) -> None:
    """Render the multi-turn chat interface with source citations."""

    # ── Display chat history ──────────────────────────────────────────────────
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                _render_sources(message["sources"])

    # ── No documents warning ──────────────────────────────────────────────────
    if pipeline is None:
        st.info("Setting up AI pipeline... Please wait.")
        return

    doc_count = pipeline.vector_store.count() if pipeline else 0
    if doc_count == 0:
        st.info(
            "No documents indexed yet. "
            "Upload files in the sidebar to get started.",
            icon="📂",
        )

    # ── Chat input ────────────────────────────────────────────────────────────
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                result = pipeline.query(prompt)

            answer = result["answer"]
            sources = result["sources"]

            st.markdown(answer)
            if sources:
                _render_sources(sources)

        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })

    # ── Clear chat button ─────────────────────────────────────────────────────
    if st.session_state.messages:
        if st.button("Clear Chat History", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()


def _render_sources(sources: list[dict]) -> None:
    """Render collapsible source citations."""
    if not sources:
        return

    with st.expander(f"📚 Sources ({len(sources)})", expanded=False):
        for i, src in enumerate(sources, 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{i}. {src['source']}**")
                if src.get("preview"):
                    st.caption(src["preview"][:200] + "...")
            with col2:
                if src.get("file_type"):
                    st.markdown(
                        f'<span class="source-badge">{src["file_type"].upper()}</span>',
                        unsafe_allow_html=True,
                    )
            if i < len(sources):
                st.divider()
