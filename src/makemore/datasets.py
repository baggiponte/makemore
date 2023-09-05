"""Data loading utilities."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, overload

import torch
from torch.utils.data import Dataset

from makemore.utils import STRING_TO_INT, Context, Index

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from typing import Literal

    try:
        from typing_extensions import Self
    except ImportError:
        from typing import Self  # type: ignore[no-redef,attr-defined]

    from torch import Tensor


def fetch_names(
    shuffle: bool = False,  # noqa: FBT001, FBT002
    seed: int | None = None,
) -> NamesDataset | tuple[Tensor, Tensor]:
    """Fetch the names dataset."""
    url = "https://raw.githubusercontent.com/karpathy/makemore/master/names.txt"

    return NamesDataset.from_url(url, shuffle=shuffle, seed=seed)


class NamesDataset(Dataset):
    """Loads sample data."""

    def __init__(
        self,
        data: Iterable[str],
        shuffle: bool = False,  # noqa: FBT001, FBT002
        seed: int | None = None,
    ) -> None:
        self.data: list[str] = list(set(data))

        if shuffle and seed is not None:
            random.seed(seed)
            random.shuffle(self.data)
        elif shuffle:
            random.shuffle(self.data)

    @classmethod
    def from_path(
        cls,
        path: Path,
        shuffle: bool = False,  # noqa: FBT001, FBT002
        seed: int | None = None,
    ) -> Self:
        """Create a NamesDataset instance from a file."""
        try:
            names = (line.lower().strip() for line in path.open("rt"))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File {path} not found.") from e

        return cls(names, shuffle=shuffle, seed=seed)

    @classmethod
    def from_url(
        cls,
        url: str,
        shuffle: bool = False,  # noqa: FBT001, FBT002
        seed: int | None = None,
    ) -> Self:
        """Create a NamesDataset instance from a URL."""
        import requests

        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            body = (
                line.decode().strip().lower()
                for line in response.iter_lines(delimiter=b"\n")
            )
            names = [line for line in body if line != ""]

        return cls(names, shuffle=shuffle, seed=seed)

    def __repr__(self) -> str:
        """Returns a string representation of the object."""
        return f"NamesDataset with {len(self)} names."

    @overload
    def get_ngrams(
        self,
        context_size: int,
        as_tensor: Literal[False],  # noqa: FBT001, FBT002
    ) -> tuple[list[Context], list[Index]]:
        ...

    @overload
    def get_ngrams(
        self,
        context_size: int,
        as_tensor: Literal[True],  # noqa: FBT001, FBT002
    ) -> tuple[Tensor, Tensor]:
        ...

    def get_ngrams(
        self,
        context_size: int = 3,
        as_tensor: bool = False,  # noqa: FBT001, FBT002
    ) -> tuple[list[Context], list[Index]] | tuple[Tensor, Tensor]:
        """Yield all ngrams."""
        inputs: list[Context] = []
        labels: list[Index] = []

        for name in self.data:
            context: list[int] = [0] * context_size
            for char in name + ".":
                index: int = STRING_TO_INT[char]
                inputs.append(Context(tuple(context)))
                labels.append(Index(index))
                context = context[1:] + [index]

        if as_tensor:
            return torch.tensor(inputs), torch.tensor(labels)
        return inputs, labels

    def __getitem__(self, index: int) -> str:
        """Loads nth ngram."""
        return self.data[index]

    def __len__(self) -> int:
        """Returns number of ngrams."""
        return len(self.data)
