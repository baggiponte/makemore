"""Data loading utilities."""

from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from torch.utils.data import Dataset

from makemore.utils import STRING_TO_INT

if TYPE_CHECKING:
    from collections.abc import Iterable


class NamesDataset(Dataset):
    """Loads sample data."""

    NAMES_URL = "https://raw.githubusercontent.com/karpathy/makemore/master/names.txt"

    def __init__(
        self,
        url: str | None = None,
        shuffle: bool = False,  # noqa: FBT001, FBT002
        seed: int | None = None,
    ) -> None:
        self.url: str = url or self.NAMES_URL
        self.data: list[str] = sorted(set(self._load_data()))

        if shuffle and seed is not None:
            random.seed(seed)
            random.shuffle(self.data)
        elif shuffle:
            random.shuffle(self.data)

    def _load_data(self) -> Iterable[str]:
        """Loads raw data."""
        datadir: Path = Path(__package__).parent.absolute().joinpath("data")
        datadir.mkdir(exist_ok=True)

        datapath: Path = datadir.joinpath(self.url.rpartition("/")[-1])

        names: Iterable[str]

        try:
            names = (line.lower().strip() for line in datapath.open("rt"))
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

    def get_ngrams(
        self, context_size: int = 3
    ) -> tuple[list[tuple[int, ...]], list[int]]:
        """Yield all ngrams."""
        inputs = []
        labels = []

        for name in self.data:
            context = [0] * context_size
            for char in name + ".":
                index = STRING_TO_INT[char]
                context = context[1:] + [index]
                inputs.append(tuple(context))
                labels.append(index)

        return inputs, labels

    def __getitem__(self, index: int) -> str:
        """Loads nth ngram."""
        return self.data[index]

    def __len__(self) -> int:
        """Returns number of ngrams."""
        return len(self.data)
