"""Module 2: tokenization.

Splits raw text into tokens. Query tokenization additionally keeps '*'
so wildcard terms survive.
"""
import re
from typing import List

_WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)*", re.UNICODE)
_QUERY_WORD = re.compile(r"[^\W_*]*\*[^\W_*]*(?:\*[^\W_*]*)*|[^\W_]+(?:'[^\W_]+)*", re.UNICODE)


def tokenize(text: str) -> List[str]:
    """Split document text into word tokens."""
    return _WORD.findall(text)


def tokenize_query(text: str, keep_wildcards: bool = True) -> List[str]:
    """Split query text into tokens, preserving '*' inside wildcard terms."""
    if keep_wildcards:
        return [t for t in _QUERY_WORD.findall(text) if t.strip("*")]
    return tokenize(text)
