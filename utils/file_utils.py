"""
utils/file_utils.py — File handling helpers
"""
from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path
from typing import Optional


def save_uploaded_file(uploaded_file, dest_dir: Path) -> Path:
    """Save a Streamlit UploadedFile to a destination directory."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / uploaded_file.name
    with open(dest_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return dest_path


def save_to_tempfile(data: bytes, suffix: str) -> Path:
    """Save bytes to a temporary file and return its path."""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, mode="wb"
    ) as tmp:
        tmp.write(data)
        return Path(tmp.name)


def hash_bytes(data: bytes) -> str:
    """Compute SHA256 hash of bytes."""
    return hashlib.sha256(data).hexdigest()


def hash_file(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_size_mb(file_path: Path) -> float:
    """Return file size in megabytes."""
    return file_path.stat().st_size / (1024 * 1024)


def clean_temp_files(directory: Path, pattern: str = "*") -> int:
    """Delete all files matching pattern in directory. Returns count deleted."""
    count = 0
    for f in directory.glob(pattern):
        if f.is_file():
            f.unlink()
            count += 1
    return count


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_extension(filename: str) -> str:
    """Return lowercase extension including the dot."""
    return Path(filename).suffix.lower()


def is_supported_file(filename: str, supported_extensions: dict) -> bool:
    """Check if a filename has a supported extension."""
    return get_extension(filename) in supported_extensions
