#!/usr/bin/env bash
# setup.sh — One-click setup for doc-ai-rag
set -e

echo "================================================"
echo "  Universal Document AI — Setup"
echo "================================================"
echo ""

# ── Check Python version ──────────────────────────────────────────────────────
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.10"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)"; then
    echo "[OK] Python $PYTHON_VERSION found"
else
    echo "[ERROR] Python 3.10+ required (found $PYTHON_VERSION)"
    exit 1
fi

# ── Check Ollama ──────────────────────────────────────────────────────────────
if command -v ollama &> /dev/null; then
    echo "[OK] Ollama found: $(ollama --version 2>/dev/null || echo 'installed')"
else
    echo "[WARN] Ollama not found."
    echo "       Install it from: https://ollama.ai"
    echo "       Then run: ollama pull llama3"
fi

# ── Create virtual environment ────────────────────────────────────────────────
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
fi

# ── Activate and install ──────────────────────────────────────────────────────
source venv/bin/activate
echo "[OK] Virtual environment activated"

echo ""
echo "Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "[OK] Dependencies installed"

# ── Copy .env ─────────────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "[OK] Created .env from .env.example"
    echo "     Edit .env to customize settings"
fi

# ── Create data directories ───────────────────────────────────────────────────
mkdir -p data/chroma_db data/uploads
echo "[OK] Data directories created"

# ── Pull default Ollama model ──────────────────────────────────────────────────
echo ""
echo "Pulling default Ollama model (llama3)..."
echo "   This may take a few minutes on first run..."
if command -v ollama &> /dev/null; then
    ollama pull llama3 && echo "[OK] llama3 model ready"
else
    echo "[SKIP] Ollama not installed — pull a model manually later"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  Setup complete!"
echo "================================================"
echo ""
echo "To start the app:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "Then open: http://localhost:8501"
echo ""
