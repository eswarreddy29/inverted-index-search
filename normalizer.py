"""Module 3: text normalization / case folding."""
import unicodedata
from typing import Iterable, List


def normalize(token: str) -> str:
    """Case-fold, apply Unicode NFKD, and strip accents and apostrophes."""
    folded = unicodedata.normalize("NFKD", token.casefold())
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    return folded.replace("'", "")


def normalize_all(tokens: Iterable[str]) -> List[str]:
    return [t for t in (normalize(tok) for tok in tokens) if t]
