"""Types."""
from __future__ import annotations

from dataclasses import dataclass
from string import ascii_lowercase

LETTERS = "." + ascii_lowercase
INT_TO_STRING = dict(enumerate(LETTERS))
STRING_TO_INT = {s: i for i, s in INT_TO_STRING.items()}


@dataclass
class ModelInput:
    """Input for an ngram model."""

    inpt: list[int]
    outpt: int

    def as_characters(self) -> tuple[list[str], str]:
        """Converts input and output to characters."""
        return [INT_TO_STRING[inpt] for inpt in self.inpt], INT_TO_STRING[self.outpt]
