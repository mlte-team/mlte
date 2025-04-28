"""Tests for basic store classes."""

import pytest

from mlte.store.base import StoreType, StoreURI


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
    [StoreURI.create_uri_string(type, "path") for type in StoreType],
)
def test_from_string_valid(uri_string: str):
    """Checks that StoreURI can be built for all store types."""
    # Test passes if no exception is thrown.
    _ = StoreURI.from_string(uri_string)


@pytest.mark.parametrize("uri_string", ["invalid", "db://", "://file"])
def test_from_string_invalid(uri_string: str):
    """Checks that StoreURI can be built for all store types."""
    with pytest.raises(RuntimeError):
        _ = StoreURI.from_string(uri_string)
