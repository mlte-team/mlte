"""
mlte/_private/text.py

Internal utilities for handling text.
"""

import textwrap


def cleantext(text: str) -> str:
    """
    Clean a text string.

    :param text: The input text
    :type text: str

    :return: The cleaned text
    :rtype: str
    """
    return " ".join(textwrap.dedent(text).strip().split("\n"))
