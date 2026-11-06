"""Module 5: query processing.

Supports boolean queries with AND / OR / NOT (precedence NOT > AND > OR).
Adjacent terms are combined with an implicit AND. Terms containing '*' are
expanded via the wildcard module and OR-ed together.
"""
from typing import List, Set, Tuple

from inverted_index import InvertedIndex
from normalizer import normalize
from tokenizer import tokenize_query
from wildcard import PermutermIndex


class QueryProcessor:
    def __init__(self, index: InvertedIndex) -> None:
        self.index = index
        self.permuterm = PermutermIndex(index.vocabulary)

    def _term_docs(self, token: str) -> Set[int]:
        term = normalize(token.replace("*", "\0")).replace("\0", "*")
        if "*" in term:
            docs: Set[int] = set()
            for match in self.permuterm.expand(term):
                docs |= self.index.docs_for(match)
            return docs
        return self.index.docs_for(term)

    def _split_or_groups(self, text: str) -> List[List[Tuple[bool, str]]]:
        """Return OR-groups; each group is a list of (negated, term) AND-ed."""
        groups: List[List[Tuple[bool, str]]] = [[]]
        negate = False
        for raw in text.split():
            word = raw.strip()
            upper = word.upper()
            if upper == "OR":
                groups.append([])
                negate = False
            elif upper == "AND":
                continue
            elif upper == "NOT":
                negate = not negate
            else:
                for tok in tokenize_query(word):
                    groups[-1].append((negate, tok))
                negate = False
        return [g for g in groups if g]

    def search(self, text: str) -> List[str]:
        """Return matching document names, sorted."""
        result: Set[int] = set()
        for group in self._split_or_groups(text):
            docs = self.index.all_docs()
            for negated, tok in group:
                matches = self._term_docs(tok)
                docs = docs - matches if negated else docs & matches
            result |= docs
        return [self.index.doc_names[d] for d in sorted(result)]
