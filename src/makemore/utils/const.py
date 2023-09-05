"""Utilities."""

from __future__ import annotations

from string import ascii_lowercase

from makemore.utils.types import AlphabetCharacter, AlphabetIndex

CHARACTER_TO_INDEX: dict[AlphabetCharacter, AlphabetIndex] = {
    AlphabetCharacter(v): AlphabetIndex(k) for k, v in enumerate("." + ascii_lowercase)
}
INDEX_TO_CHARACTER: dict[AlphabetIndex, AlphabetCharacter] = {
    AlphabetIndex(k): AlphabetCharacter(v) for k, v in enumerate("." + ascii_lowercase)
}


def character_to_int(character: AlphabetCharacter) -> AlphabetIndex:
    """Convert a character to an integer."""
    return AlphabetIndex(CHARACTER_TO_INDEX[character])


def int_to_character(index: AlphabetIndex) -> AlphabetCharacter:
    """Convert an integer to a character."""
    return AlphabetCharacter(INDEX_TO_CHARACTER[index])
