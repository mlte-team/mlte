"""Utilities related to measurement collection."""

from collections.abc import Iterable
from typing import Any


def flatten(*collections: Any | Iterable[Any]) -> list[Any]:
    """
    Flatten a variadic number of collections.

    :param collections: The collections to flatten

    :return: The flattened collection
    """
    clone = [collection for collection in collections]
    for i, _ in enumerate(clone):
        while i < len(clone) and isinstance(clone[i], (list, tuple)):
            clone[i : i + 1] = clone[i]  # noqa
    return clone
