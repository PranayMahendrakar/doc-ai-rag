"""
core/rag_pipeline.py — LangChain RAG chain with source citations
"""
from __future__ import annotations

from typing import Dict, Any, List, Optional

from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import Document
from langchain_core.language_models import BaseLLM
from loguru import logger

import config
from core.vector_store import VectorStoreManager


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline.
    
    Retrieves relevant document chunks from ChromaDB,
    then generates answers using a local Ollama LLM.
    """

    def __init__(
        self,
        vector_store: VectorStoreManager,
        llm: BaseLLM,
        top_k: int = config.TOP_K,
        system_prompt: str = config.RAG_SYSTEM_PROMPT,
    ):
        self.vector_store = vector_store
        self.llm = llm
        self.top_k = top_k
        self.system_prompt = system_prompt
        self._chain = self._build_chain()

    def _build_chain(self) -> BaseRetrievalQA:
        """Build the LangChain RetrievalQA chain."""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template(config.RAG_HUMAN_PROMPT),
        ])

        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(k=self.top_k),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )
        return chain

    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG pipeline.
        
        Returns:
            dict with keys:
                - answer: str
                - sources: List[Dict] with source metadata
                - num_sources: int
        """
        if self.vector_store.count() == 0:
            return {
                "answer": "No documents have been uploaded yet. Please upload some documents first.",
                "sources": [],
                "num_sources": 0,
            }

        try:
            logger.info(f"Querying RAG: {question[:80]}...")
            result = self._chain.invoke({"query": question})

            answer = result.get("result", "No answer generated.")
            source_docs: List[Document] = result.get("source_documents", [])

            # Deduplicate sources by filename
            seen_sources = set()
            sources = []
            for doc in source_docs:
                src = doc.metadata.get("source", "unknown")
                if src not in seen_sources:
                    seen_sources.add(src)
                    sources.append({
                        "source": src,
                        "file_type": doc.metadata.get("file_type", ""),
                        "chunk_index": doc.metadata.get("chunk_index", 0),
                        "preview": doc.page_content[:200].strip(),
                    })

            logger.success(f"RAG answer generated from {len(sources)} source(s)")
            return {
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources),
            }

        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": [],
                "num_sources": 0,
            }

    def update_model(self, new_llm: BaseLLM) -> None:
        """Swap the LLM and rebuild the chain."""
        self.llm = new_llm
        self._chain = self._build_chain()
        logger.info("RAG pipeline updated with new LLM")
