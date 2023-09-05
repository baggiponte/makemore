"""Custom types."""
from __future__ import annotations

from typing import NewType

AlphabetIndex = NewType("AlphabetIndex", int)
AlphabetCharacter = NewType("AlphabetCharacter", str)
Context = NewType("Context", tuple[AlphabetIndex, ...])
