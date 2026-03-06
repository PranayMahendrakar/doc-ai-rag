"""
core/document_loader.py — Multi-format document ingestion for doc-ai-rag

Supports: PDF, DOCX, CSV, TXT, MD, and source code files.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

import config


class DocumentLoader:
    """Loads and splits documents from various file formats."""

    # Map extension to loader class
    LOADERS = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".doc": Docx2txtLoader,
        ".csv": CSVLoader,
        ".md": UnstructuredMarkdownLoader,
    }

    def __init__(
        self,
        chunk_size: int = config.CHUNK_SIZE,
        chunk_overlap: int = config.CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            length_function=len,
        )

    def load_file(self, file_path: str | Path) -> List[Document]:
        """Load a single file and return list of Document chunks."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = file_path.suffix.lower()
        logger.info(f"Loading {file_path.name} (extension: {extension})")

        try:
            documents = self._load_by_extension(file_path, extension)
            chunks = self.text_splitter.split_documents(documents)

            # Enrich metadata
            file_hash = self._hash_file(file_path)
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "source": file_path.name,
                    "file_path": str(file_path),
                    "file_hash": file_hash,
                    "file_type": extension.lstrip("."),
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                })

            logger.success(f"Loaded {file_path.name}: {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"Failed to load {file_path.name}: {e}")
            raise

    def _load_by_extension(
        self, file_path: Path, extension: str
    ) -> List[Document]:
        """Route file to appropriate loader."""
        if extension in self.LOADERS:
            loader_cls = self.LOADERS[extension]
            loader = loader_cls(str(file_path))
            return loader.load()

        # Fallback: treat as plain text (covers .py, .js, .ts, .txt, .json, etc.)
        try:
            loader = TextLoader(str(file_path), encoding="utf-8")
            return loader.load()
        except UnicodeDecodeError:
            loader = TextLoader(str(file_path), encoding="latin-1")
            return loader.load()

    @staticmethod
    def _hash_file(file_path: Path) -> str:
        """Compute SHA256 hash of a file for deduplication."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def load_multiple(self, file_paths: List[str | Path]) -> List[Document]:
        """Load multiple files and return combined chunks."""
        all_chunks: List[Document] = []
        for path in file_paths:
            try:
                chunks = self.load_file(path)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.warning(f"Skipping {path}: {e}")
        return all_chunks
