"""
core/embeddings.py — Local embedding model wrapper using sentence-transformers
"""
from __future__ import annotations

from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from loguru import logger

import config


class EmbeddingManager:
    """Manages local sentence-transformer embeddings."""

    _instance: "EmbeddingManager | None" = None
    _embeddings: HuggingFaceEmbeddings | None = None

    def __new__(cls, *args, **kwargs):
        """Singleton to avoid reloading the model on every call."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        model_name: str = config.EMBEDDING_MODEL,
        device: str = config.EMBEDDING_DEVICE,
    ):
        if self._embeddings is not None:
            return  # Already initialized

        logger.info(f"Loading embedding model: {model_name} on {device}")
        self._embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True},
        )
        logger.success(f"Embedding model loaded: {model_name}")

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """Return the LangChain-compatible embeddings object."""
        return self._embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        return self._embeddings.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document strings."""
        return self._embeddings.embed_documents(texts)

    @property
    def model_name(self) -> str:
        return self._embeddings.model_name if self._embeddings else "not loaded"
