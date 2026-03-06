"""
core/ollama_client.py — Ollama LLM client wrapper for LangChain
"""
from __future__ import annotations

import httpx
from langchain_ollama import OllamaLLM
from loguru import logger

import config


class OllamaClient:
    """
    Wraps the Ollama local LLM server.
    
    Provides model listing, health checking, and LangChain LLM object creation.
    """

    def __init__(
        self,
        base_url: str = config.OLLAMA_BASE_URL,
        model: str = config.OLLAMA_MODEL,
        temperature: float = config.OLLAMA_TEMPERATURE,
        timeout: int = config.OLLAMA_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self._llm: OllamaLLM | None = None

    def get_llm(self) -> OllamaLLM:
        """Return (or create) a LangChain Ollama LLM instance."""
        if self._llm is None or self._llm.model != self.model:
            self._llm = OllamaLLM(
                base_url=self.base_url,
                model=self.model,
                temperature=self.temperature,
                timeout=self.timeout,
            )
            logger.info(f"Ollama LLM configured: model={self.model}")
        return self._llm

    def is_available(self) -> bool:
        """Check if the Ollama server is reachable."""
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """Return list of available model names from Ollama."""
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception as e:
            logger.warning(f"Could not fetch Ollama models: {e}")
            return [self.model]

    def set_model(self, model: str) -> None:
        """Switch to a different Ollama model."""
        self.model = model
        self._llm = None  # Force recreation on next get_llm() call
        logger.info(f"Ollama model switched to: {model}")

    def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama registry (may take a while)."""
        try:
            response = httpx.post(
                f"{self.base_url}/api/pull",
                json={"name": model},
                timeout=None,  # Pulling can take a long time
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False
