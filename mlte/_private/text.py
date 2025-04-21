"""Internal utilities for handling text."""

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


def replace_all(
    main_string: str, replacements: dict[str, str], revert: bool = False
) -> str:
    """
    Replaces all instances of the given strings with the provided replacements.

    :param main_string: the string to do the replacements on.
    :param replacement: a dict of substrings and their replacements.
    :param revert: if true, revert how the replacements dict is used: the replacements will be found and replaced with the substrings.
    """
    for substring, replacement in replacements.items():
        if not revert:
            to_find = substring
            to_put = replacement
        else:
            to_find = replacement
            to_put = substring
        main_string = main_string.replace(to_find, to_put)
    return main_string
