"""Module 4: inverted index construction."""
from collections import defaultdict
from typing import Dict, List, Set

from normalizer import normalize_all
from tokenizer import tokenize


class InvertedIndex:
    """Maps term -> sorted postings list of doc ids (with term positions)."""

    def __init__(self) -> None:
        self.doc_names: List[str] = []
        self.postings: Dict[str, Dict[int, List[int]]] = defaultdict(dict)

    def build(self, documents: Dict[str, str]) -> "InvertedIndex":
        for doc_id, (name, text) in enumerate(documents.items()):
            self.doc_names.append(name)
            terms = normalize_all(tokenize(text))
            for pos, term in enumerate(terms):
                self.postings[term].setdefault(doc_id, []).append(pos)
        return self

    @property
    def vocabulary(self) -> List[str]:
        return sorted(self.postings)

    def all_docs(self) -> Set[int]:
        return set(range(len(self.doc_names)))

    def docs_for(self, term: str) -> Set[int]:
        return set(self.postings.get(term, {}))
