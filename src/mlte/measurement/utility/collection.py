"""
Utilities related to measurement collection.
"""

from typing import Union, Any, Iterable, List


def flatten(*collections: Union[Any, Iterable[Any]]) -> List[Any]:
    """
    Flatten a variadic number of collections.

    :param collections: The collections to flatten
    :type collections: Union[Any, Iterable[Any]]

    :return: The flattened collection
    :rtype: List[Any]
    """
    clone = [collection for collection in collections]
    for i, _ in enumerate(clone):
        while i < len(clone) and isinstance(clone[i], (list, tuple)):
            clone[i : i + 1] = clone[i]  # noqa
    return clone
