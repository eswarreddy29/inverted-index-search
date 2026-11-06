"""Module 6: wildcard processing using a permuterm index.

Every term t is stored as all rotations of t + '$'. A wildcard query such as
"mon*ey" is rotated so the '*' is at the end ("ey$mon*"), which turns it into
a prefix lookup on the sorted permuterm list (binary search).
"""
import re
from bisect import bisect_left
from typing import Iterable, List, Set, Tuple


class PermutermIndex:
    def __init__(self, vocabulary: Iterable[str]) -> None:
        entries: List[Tuple[str, str]] = []
        for term in vocabulary:
            extended = term + "$"
            for i in range(len(extended)):
                entries.append((extended[i:] + extended[:i], term))
        entries.sort()
        self._keys = [k for k, _ in entries]
        self._terms = [t for _, t in entries]

    def _prefix_lookup(self, prefix: str) -> Set[str]:
        found: Set[str] = set()
        i = bisect_left(self._keys, prefix)
        while i < len(self._keys) and self._keys[i].startswith(prefix):
            found.add(self._terms[i])
            i += 1
        return found

    def expand(self, pattern: str) -> Set[str]:
        """Return all vocabulary terms matching a pattern containing '*'."""
        if "*" not in pattern:
            return self._prefix_lookup(pattern + "$")

        extended = pattern + "$"
        star = extended.index("*")
        # Rotate so text after the first '*' comes first: X*Y$ -> Y$X
        prefix = extended[star + 1:] + extended[:star]
        candidates = self._prefix_lookup(prefix)

        if pattern.count("*") == 1:
            return candidates
        # Several wildcards: the prefix lookup is only a filter, verify with regex.
        regex = re.compile("^" + ".*".join(re.escape(p) for p in pattern.split("*")) + "$")
        return {t for t in candidates if regex.match(t)}
