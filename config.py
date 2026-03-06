"""
config.py — Central configuration for doc-ai-rag
All settings can be overridden via environment variables or .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_PERSIST_DIR = DATA_DIR / os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
UPLOAD_DIR = DATA_DIR / "uploads"

# Create directories if they don't exist
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ─── Ollama ───────────────────────────────────────────────────────────────────
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# ─── Embeddings ───────────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DEVICE: str = os.getenv("EMBEDDING_DEVICE", "cpu")  # cpu or cuda

# ─── Text Splitting ───────────────────────────────────────────────────────────
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

# ─── Retrieval ────────────────────────────────────────────────────────────────
TOP_K: int = int(os.getenv("TOP_K", "5"))
SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))

# ─── Collection ───────────────────────────────────────────────────────────────
CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "documents")

# ─── Supported File Types ─────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {
    # Documents
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx",
    # Spreadsheets
    ".csv": "csv",
    ".xlsx": "excel",
    # Text
    ".txt": "text",
    ".md": "markdown",
    # Code
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".sh": "bash",
    # Data
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".xml": "xml",
    ".html": "html",
    ".css": "css",
}

SUPPORTED_MIME_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
    "text/csv",
    "application/json",
    "text/x-python",
    "text/javascript",
]

# ─── RAG Prompt ───────────────────────────────────────────────────────────────
RAG_SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided document context.

Instructions:
- Answer questions ONLY based on the provided context.
- If the context doesn't contain enough information to answer, say so clearly.
- Always cite the source document(s) when possible.
- Be concise but thorough in your responses.
- If asked for code, format it properly.

Context:
{context}"""

RAG_HUMAN_PROMPT = "{question}"

# ─── UI Settings ──────────────────────────────────────────────────────────────
APP_TITLE = "Universal Document AI"
APP_ICON = "📄"
APP_DESCRIPTION = "Upload documents and ask questions — fully local, fully private."
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
