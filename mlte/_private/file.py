REPLACE_CHARS = {"/": "__"}
"""Chars that need replacing, and their replacements."""


def make_valid_filename(filename: str) -> str:
    """Cleans the given filename so it is a valid one."""
    for char, replacement in REPLACE_CHARS.items():
        filename = filename.replace(char, replacement)
    return filename


def revert_valid_filename(filename: str) -> str:
    """Undo the cleanup done by make_valid_filename."""
    for char, replacement in REPLACE_CHARS.items():
        filename = filename.replace(replacement, char)
    return filename
