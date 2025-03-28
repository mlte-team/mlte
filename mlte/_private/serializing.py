"""
mlte/_private/serializing.py

Internal utilities for serializing code.
"""

import base64
import typing
from typing import Any, Callable

import dill  # type: ignore


def encode_callable(callable: Callable[[Any], Any]) -> str:
    """
    Encodes the callable as a base64 string.

    :param callable: A callable function.
    :return: A string with the base64 representation of the dilled function.
    """
    return base64.b64encode(dill.dumps(callable)).decode("utf-8")


def decode_callable(encoded_callable: str) -> Callable[[Any], Any]:
    """
    Decodes the callable from a base64 string.

    :param encoded_callable: A string with the base64 representation of a dilled function.
    :return: A callable function.
    """
    return typing.cast(
        Callable[[Any], Any],
        dill.loads(base64.b64decode(encoded_callable.encode("utf-8"))),
    )
