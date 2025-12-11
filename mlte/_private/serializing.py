"""Internal utilities for serializing code."""

import base64
import typing
from typing import Any, Callable

import dill  # type: ignore


def encode_callable(callable: Callable[..., Any]) -> str:
    """
    Encodes the callable as a base64 string.

    :param callable: A callable function.
    :return: A string with the base64 representation of the dilled function.
    """
    return base64.b64encode(dill.dumps(callable)).decode("utf-8")


def decode_callable(encoded_callable: str) -> Callable[..., Any]:
    """
    Decodes the callable from a base64 string.

    :param encoded_callable: A string with the base64 representation of a dilled function.
    :return: A callable function.
    """
    return typing.cast(
        Callable[..., Any],
        dill.loads(base64.b64decode(encoded_callable.encode("utf-8"))),
    )


def compare_callable(c1: Callable[..., Any], c2: Callable[..., Any]) -> bool:
    """
    Compares two callables.

    :param c1, c2: Two callables to compare.
    :return: True if equal in code, false if not.
    """
    return c1.__code__ == c2.__code__
