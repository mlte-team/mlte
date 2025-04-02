"""
Various file-related utils.
"""

from mlte._private import text

VALID_FILE_REPLACEMENTS = {"/": "___"}
"""Chars that need replacing, and their replacements."""


def make_valid_filename(filename: str) -> str:
    """Cleans the given filename so it is a valid one."""
    return text.replace_all(filename, VALID_FILE_REPLACEMENTS)


def revert_valid_filename(filename: str) -> str:
    """Undo the cleanup done by make_valid_filename."""
    return text.replace_all(filename, VALID_FILE_REPLACEMENTS, revert=True)
