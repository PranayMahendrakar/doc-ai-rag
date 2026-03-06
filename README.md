# 📄 Universal Document AI — Local RAG System

> Upload documents. Ask questions. Get answers — fully local, fully private.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-purple.svg)](https://trychroma.com)
[![Ollama](https://img.shields.io/badge/Ollama-local-orange.svg)](https://ollama.ai)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Overview

**doc-ai-rag** is a fully local, privacy-first Retrieval-Augmented Generation (RAG) system. Upload your PDFs, Word documents, CSVs, or source code files and instantly query them with a conversational AI — powered by **Ollama** (no API keys needed, no data leaves your machine).

---

## ✨ Features

| Feature | Details |
|---|---|
| 📁 Multi-format Upload | PDF, DOCX, CSV, TXT, Python, JS, and more |
| 🔍 Semantic Search | Dense vector similarity via sentence-transformers |
| 🤖 LLM Answers | Local LLMs via Ollama (llama3, mistral, phi3) |
| 🗄️ Vector Database | ChromaDB — persistent, fast, local |
| 🧩 Modular RAG Pipeline | LangChain orchestration with source citations |
| 💬 Chat UI | Streamlit multi-turn conversational interface |
| 📊 Document Manager | View, delete, and inspect indexed documents |
| 🔒 100% Local | No OpenAI keys, no cloud calls |

---

## 🛠️ Tech Stack

- **LangChain** — document loaders, text splitters, retrieval chains
- **ChromaDB** — local persistent vector store
- **Ollama** — run LLMs locally (llama3, mistral, phi3, gemma2)
- **sentence-transformers** — local embedding models (all-MiniLM-L6-v2)
- **Streamlit** — clean, fast Python web UI

---

## 📁 Project Structure

```
doc-ai-rag/
├── app.py                    # Streamlit entry point
├── config.py                 # Central configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # One-click setup script
├── Dockerfile                # Docker container
├── docker-compose.yml        # Docker Compose
├── .env.example              # Environment variables template
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── document_loader.py    # Multi-format document ingestion
│   ├── embeddings.py         # Local embedding model wrapper
│   ├── vector_store.py       # ChromaDB vector store manager
│   ├── rag_pipeline.py       # LangChain RAG chain
│   └── ollama_client.py      # Ollama LLM wrapper
│
├── ui/
│   ├── __init__.py
│   ├── sidebar.py            # Upload & settings sidebar
│   ├── chat.py               # Chat interface component
│   └── document_manager.py   # Document list & management
│
└── utils/
    ├── __init__.py
    ├── file_utils.py         # File handling helpers
    └── text_utils.py         # Text processing utilities
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- At least one Ollama model pulled

### 1. Clone & Setup

```bash
git clone https://github.com/PranayMahendrakar/doc-ai-rag.git
cd doc-ai-rag
bash setup.sh
```

### 2. Pull an Ollama model

```bash
ollama pull llama3
```

### 3. Run

```bash
source venv/bin/activate
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## 🔧 Configuration

| Variable | Default | Description |
|---|---|---|
| OLLAMA_MODEL | llama3 | Ollama model to use |
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama server URL |
| EMBEDDING_MODEL | all-MiniLM-L6-v2 | Embedding model |
| CHUNK_SIZE | 1000 | Text chunk size |
| CHUNK_OVERLAP | 200 | Overlap between chunks |
| TOP_K | 5 | Number of chunks to retrieve |

---

## 📚 Supported File Types

PDF, DOCX, CSV, TXT, MD, PY, JS, TS, JAVA, CPP, GO, RS, JSON, YAML, XML

---

## 🎯 Use Cases

- **Students** — Chat with lecture notes, papers, and textbooks
- **Researchers** — Query a corpus of academic PDFs
- **Developers** — Ask questions about a codebase
- **Companies** — Internal document Q&A without data leaving premises
- **Analysts** — Interrogate CSV reports conversationally

---

## 🗺️ Roadmap

- [ ] Multi-document cross-referencing
- [ ] React frontend alternative
- [ ] GPU-accelerated embeddings
- [ ] OCR support for scanned PDFs
- [ ] REST API mode
- [ ] Web page ingestion (URL input)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">Built with ❤️ using LangChain · ChromaDB · Ollama · Streamlit</p># test content# 📄 Universal Document AI — Local RAG System

> Upload documents. Ask questions. Get answers — fully local, fully private.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-purple.svg)](https://trychroma.com)
[![Ollama](https://img.shields.io/badge/Ollama-local-orange.svg)](https://ollama.ai)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Overview

**doc-ai-rag** is a fully local, privacy-first Retrieval-Augmented Generation (RAG) system. Upload your PDFs, Word documents, CSVs, or source code files and instantly query them with a conversational AI — powered by **Ollama** (no API keys needed, no data leaves your machine).

---

## ✨ Features

| Feature | Details |
|---|---|
| 📁 Multi-format Upload | PDF, DOCX, CSV, TXT, Python, JS, and more |
| 🔍 Semantic Search | Dense vector similarity via sentence-transformers |
| 🤖 LLM Answers | Local LLMs via Ollama (llama3, mistral, phi3) |
| 🗄️ Vector Database | ChromaDB — persistent, fast, local |
| 🧩 Modular RAG Pipeline | LangChain orchestration with source citations |
| 💬 Chat UI | Streamlit multi-turn conversational interface |
| 📊 Document Manager | View, delete, and inspect indexed documents |
| 🔒 100% Local | No OpenAI keys, no cloud calls |

---

## 🛠️ Tech Stack

- **LangChain** — document loaders, text splitters, retrieval chains
- **ChromaDB** — local persistent vector store
- **Ollama** — run LLMs locally (llama3, mistral, phi3, gemma2)
- **sentence-transformers** — local embedding models (all-MiniLM-L6-v2)
- **Streamlit** — clean, fast Python web UI

---

## 📁 Project Structure

```
doc-ai-rag/
├── app.py                    # Streamlit entry point
├── config.py                 # Central configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # One-click setup script
├── Dockerfile                # Docker container
├── docker-compose.yml        # Docker Compose
├── .env.example              # Environment variables template
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── document_loader.py    # Multi-format document ingestion
│   ├── embeddings.py         # Local embedding model wrapper
│   ├── vector_store.py       # ChromaDB vector store manager
│   ├── rag_pipeline.py       # LangChain RAG chain
│   └── ollama_client.py      # Ollama LLM wrapper
│
├── ui/
│   ├── __init__.py
│   ├── sidebar.py            # Upload & settings sidebar
│   ├── chat.py               # Chat interface component
│   └── document_manager.py   # Document list & management
│
└── utils/
    ├── __init__.py
    ├── file_utils.py         # File handling helpers
    └── text_utils.py         # Text processing utilities
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- At least one Ollama model pulled

### 1. Clone & Install

```bash
git clone https://github.com/PranayMahendrakar/doc-ai-rag.git
cd doc-ai-rag
pip install -r requirements.txt
```

### 2. Pull an Ollama model

```bash
ollama pull llama3
```

### 3. Run

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## 🔧 Configuration

| Variable | Default | Description |
|---|---|---|
| OLLAMA_MODEL | llama3 | Ollama model to use |
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama server URL |
| EMBEDDING_MODEL | all-MiniLM-L6-v2 | Embedding model |
| CHUNK_SIZE | 1000 | Text chunk size |
| CHUNK_OVERLAP | 200 | Overlap between chunks |
| TOP_K | 5 | Number of chunks to retrieve |

---

## 📚 Supported File Types

PDF, DOCX, CSV, TXT, MD, PY, JS, TS, JAVA, CPP, GO, RS, JSON, YAML, XML

---

## 🎯 Use Cases

- **Students** — Chat with lecture notes, papers, and textbooks
- **Researchers** — Query a corpus of academic PDFs
- **Developers** — Ask questions about a codebase
- **Companies** — Internal document Q&A without data leaving premises
- **Analysts** — Interrogate CSV reports conversationally

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">Built with LangChain · ChromaDB · Ollama · Streamlit</p>
