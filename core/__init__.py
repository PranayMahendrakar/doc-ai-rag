"""core — Document ingestion, embeddings, vector store, and RAG pipeline."""
from core.document_loader import DocumentLoader
from core.embeddings import EmbeddingManager
from core.vector_store import VectorStoreManager
from core.rag_pipeline import RAGPipeline
from core.ollama_client import OllamaClient

__all__ = [
    "DocumentLoader",
    "EmbeddingManager", 
    "VectorStoreManager",
    "RAGPipeline",
    "OllamaClient",
]
