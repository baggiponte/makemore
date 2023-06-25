"""Data loading utilities."""

from __future__ import annotations

from importlib import resources
from typing import TYPE_CHECKING

import requests
from more_itertools import nth
from torch.utils.data import Dataset

import makemore.data
from makemore.types import STRING_TO_INT, ModelInput

if TYPE_CHECKING:
    from collections.abc import Iterable
    from importlib.abc import Traversable


class NamesDataset(Dataset):
    """Loads sample data."""

    NAMES_URL = "https://raw.githubusercontent.com/karpathy/makemore/master/names.txt"

    def __init__(self, url: str | None = None, context_size: int = 3) -> None:
        self.url: str = url or self.NAMES_URL
        self.size: int = context_size

    @property
    def data(self) -> Iterable[str]:
        """Loads raw data."""
        datadir: Traversable = resources.files(makemore.data).joinpath(
            self.url.rpartition("/")[-1]
        )

        names: Iterable[str]

        try:
            names = (line.lower().strip() for line in datadir.open("rt"))
        except FileNotFoundError:
            with (
                requests.get(self.url, stream=True, timeout=30) as response,
                datadir.open("wb") as file,
            ):
                response.raise_for_status()

                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            names = (line.lower().strip() for line in datadir.open("rt"))

        yield from names

    @property
    def ngrams(self) -> Iterable[ModelInput]:
        """Yield all ngrams."""
        for name in self.data:
            context = [0] * self.size
            for char in name + ".":
                index = STRING_TO_INT[char]
                context = context[1:] + [index]

                yield ModelInput(context, index)

    def __getitem__(self, index: int) -> ModelInput:
        """Loads nth ngram."""
        result = nth(self.ngrams, index)

        if result is None:
            raise IndexError(f"Index {index} out of range")

        return result
