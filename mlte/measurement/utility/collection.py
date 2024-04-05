"""
mlte/measurement/utility/collection.py

Utilities related to measurement collection.
"""

from typing import Any, Iterable, List, Union


def flatten(*collections: Union[Any, Iterable[Any]]) -> List[Any]:
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
