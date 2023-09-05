"""Custom types."""
from __future__ import annotations

from typing import NewType

Context = NewType("Context", tuple[int, ...])
Index = NewType("Index", int)
