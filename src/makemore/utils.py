"""Utilities."""

from __future__ import annotations

from string import ascii_lowercase

VOCABULARY = "." + ascii_lowercase
INT_TO_STRING = dict(enumerate(VOCABULARY))
STRING_TO_INT = {v: k for k, v in INT_TO_STRING.items()}
