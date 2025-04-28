"""Tests for basic store classes."""

import pytest

from mlte.store.base import StoreURI


@pytest.mark.parametrize(
    "prefix",
    [
        prefix
        for _, prefixes in StoreURI.PREFIXES.items()
        for prefix in prefixes
    ],
)
def test_type_known_prefixes(prefix: str):
    """Checks that known prefixes are properly obtained."""
    # Test passes if no exception is thrown.
    _ = StoreURI.get_type(prefix)


@pytest.mark.parametrize("prefix", ["invalid", "db", "file"])
def test_type_unknown_prefixes(prefix: str):
    """Checks that invalid prefixes are found."""
    with pytest.raises(RuntimeError):
        _ = StoreURI.get_type(prefix)


@pytest.mark.parametrize(
    "uri_string",
    [
        StoreURI.create_uri_string(prefix, "path")
        for _, prefixes in StoreURI.PREFIXES.items()
        for prefix in prefixes
    ],
)
def test_from_string_valid(uri_string: str):
    """Checks that known prefixes are properly obtained."""
    # Test passes if no exception is thrown.
    _ = StoreURI.from_string(uri_string)
