"""
core/vector_store.py — ChromaDB vector store manager
"""
from __future__ import annotations

from typing import List, Dict, Any, Optional

import chromadb
from langchain_chroma import Chroma
from langchain.schema import Document
from loguru import logger

import config
from core.embeddings import EmbeddingManager


class VectorStoreManager:
    """Manages ChromaDB vector store: add, search, delete documents."""

    def __init__(
        self,
        persist_dir: str = str(config.CHROMA_PERSIST_DIR),
        collection_name: str = config.CHROMA_COLLECTION_NAME,
        embedding_model: str = config.EMBEDDING_MODEL,
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name

        # Initialize embeddings
        em = EmbeddingManager(model_name=embedding_model)
        self.embeddings = em.get_embeddings()

        # Initialize Chroma
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._store = Chroma(
            client=self._client,
            collection_name=collection_name,
            embedding_function=self.embeddings,
        )
        logger.success(
            f"VectorStore ready: collection='{collection_name}' "
            f"docs={self.count()}"
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add document chunks to the vector store. Returns list of IDs."""
        if not documents:
            return []
        ids = self._store.add_documents(documents)
        logger.info(f"Added {len(documents)} chunks to vector store")
        return ids

    def similarity_search(
        self,
        query: str,
        k: int = config.TOP_K,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """Retrieve top-k similar documents for a query."""
        return self._store.similarity_search(query, k=k, filter=filter)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = config.TOP_K,
    ) -> List[tuple[Document, float]]:
        """Retrieve top-k similar documents with relevance scores."""
        return self._store.similarity_search_with_relevance_scores(query, k=k)

    def delete_by_source(self, source_name: str) -> int:
        """Delete all chunks belonging to a specific source file."""
        collection = self._client.get_collection(self.collection_name)
        results = collection.get(where={"source": source_name})
        ids = results.get("ids", [])
        if ids:
            collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} chunks for source: {source_name}")
        return len(ids)

    def get_all_sources(self) -> List[Dict[str, Any]]:
        """Return a list of unique indexed documents with metadata."""
        collection = self._client.get_collection(self.collection_name)
        results = collection.get(include=["metadatas"])
        metadatas = results.get("metadatas", [])

        seen = {}
        for meta in metadatas:
            source = meta.get("source", "unknown")
            if source not in seen:
                seen[source] = {
                    "source": source,
                    "file_type": meta.get("file_type", "unknown"),
                    "total_chunks": meta.get("total_chunks", 0),
                    "file_hash": meta.get("file_hash", ""),
                }
        return list(seen.values())

    def source_exists(self, file_hash: str) -> bool:
        """Check if a document with the given hash already exists."""
        collection = self._client.get_collection(self.collection_name)
        results = collection.get(where={"file_hash": file_hash}, limit=1)
        return len(results.get("ids", [])) > 0

    def count(self) -> int:
        """Return total number of chunks in the store."""
        try:
            collection = self._client.get_collection(self.collection_name)
            return collection.count()
        except Exception:
            return 0

    def reset(self) -> None:
        """Delete the entire collection (destructive!)."""
        self._client.delete_collection(self.collection_name)
        self._store = Chroma(
            client=self._client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
        )
        logger.warning("Vector store reset — all documents deleted")

    def as_retriever(self, k: int = config.TOP_K):
        """Return a LangChain retriever for use in chains."""
        return self._store.as_retriever(search_kwargs={"k": k})
