"""
utils/text_utils.py — Text processing utilities
"""
from __future__ import annotations

import re
from typing import List


def clean_text(text: str) -> str:
    """Remove excessive whitespace and normalize line endings."""
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove trailing whitespace on each line
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def truncate_text(text: str, max_chars: int = 500, suffix: str = "...") -> str:
    """Truncate text to max_chars, appending suffix if truncated."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - len(suffix)] + suffix


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract simple keywords by frequency (no external NLP required)."""
    # Remove punctuation and lowercase
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    # Filter stop words
    stop_words = {
        "the", "and", "for", "are", "was", "were", "this", "that",
        "with", "from", "have", "has", "had", "not", "but", "they",
        "which", "can", "will", "what", "how", "when", "where", "who",
        "its", "our", "your", "their", "been", "being", "also", "than",
        "into", "about", "more", "some", "such", "each", "there",
    }
    filtered = [w for w in words if w not in stop_words]
    # Count frequency
    freq: dict[str, int] = {}
    for word in filtered:
        freq[word] = freq.get(word, 0) + 1
    # Sort by frequency
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def format_answer_markdown(answer: str) -> str:
    """Ensure the answer is properly formatted as markdown."""
    # Ensure code blocks are properly fenced
    answer = re.sub(r"(?<!`)`(?!`)", "`", answer)
    return answer.strip()


def count_tokens_approx(text: str) -> int:
    """Approximate token count (roughly 4 chars per token)."""
    return len(text) // 4


def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using simple regex."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def sanitize_filename(filename: str) -> str:
    """Remove characters that are unsafe for filenames."""
    # Replace spaces and special chars with underscores
    sanitized = re.sub(r"[^\w\-.]", "_", filename)
    # Remove multiple consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized)
    return sanitized.strip("_")
