"""Module 1: document loading.

Loads plain-text documents from a directory and assigns each a doc id.
Falls back to a small built-in sample corpus when the directory is missing.
"""
from pathlib import Path
from typing import Dict

SAMPLE_DOCUMENTS = {
    "doc1.txt": "The quick brown fox jumps over the lazy dog.",
    "doc2.txt": "Never jump over the lazy dog quickly.",
    "doc3.txt": "A monkey and a donkey met a fox near the money market.",
    "doc4.txt": "Information retrieval builds an inverted index of terms.",
    "doc5.txt": "Wildcard queries like mon* or *key match many terms.",
}


def load_documents(directory: str = "documents") -> Dict[str, str]:
    """Return {doc_name: text}. Reads every .txt file under `directory`."""
    path = Path(directory)
    if not path.is_dir():
        return dict(SAMPLE_DOCUMENTS)

    docs: Dict[str, str] = {}
    for file in sorted(path.rglob("*.txt")):
        try:
            docs[str(file.relative_to(path))] = file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue  # skip unreadable files
    return docs or dict(SAMPLE_DOCUMENTS)
