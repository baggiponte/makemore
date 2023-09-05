"""Utilities."""

from __future__ import annotations

from string import ascii_lowercase

VOCABULARY: str = "." + ascii_lowercase
INT_TO_STRING: dict[int, str] = dict(enumerate(VOCABULARY))
STRING_TO_INT: dict[str, int] = {v: k for k, v in INT_TO_STRING.items()}
