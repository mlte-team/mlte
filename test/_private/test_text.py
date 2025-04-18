"""
Unit test for the text util module.
"""

import pytest

from mlte._private import text


@pytest.mark.parametrize(
    "string,replacements,revert,expected",
    [
        ("no_invalid_chars", {"/": "-", "*": ":"}, False, "no_invalid_chars"),
        (
            "two_invalid/chars*",
            {"/": "-", "*": ":"},
            False,
            "two_invalid-chars:",
        ),
        (
            "longer_substrings//chars***oo",
            {"//": "-", "***": ":-"},
            False,
            "longer_substrings-chars:-oo",
        ),
        (
            "two_invalid-chars:",
            {"/": "-", "*": ":"},
            True,
            "two_invalid/chars*",
        ),
    ],
)
def test_replace_all(
    string: str, replacements: dict[str, str], revert: bool, expected: str
):
    """Test that replacement works as expected."""
    replaced = text.replace_all(string, replacements, revert)
    assert replaced == expected
