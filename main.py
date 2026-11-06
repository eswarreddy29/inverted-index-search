"""Entry point: wires the modules together.

Usage: python main.py [documents_directory]
"""
import sys

import gui
from document_loader import load_documents
from inverted_index import InvertedIndex
from query_processor import QueryProcessor


def build_processor(directory: str = "documents") -> QueryProcessor:
    documents = load_documents(directory)
    index = InvertedIndex().build(documents)
    return QueryProcessor(index)


if __name__ == "__main__":
    gui.run(build_processor(sys.argv[1] if len(sys.argv) > 1 else "documents"))
