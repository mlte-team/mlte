"""
test/web/store/test_util_origin.py

Unit tests for origin utility functionality.
"""

from typing import List

from mlte.backend.util.origins import is_localhost, resolve_hosts


def test_localhost_identitification() -> None:
    """Verify that localhost identification behaves as expected."""
    assert is_localhost("http://localhost:8080")
    assert not is_localhost("http://127.0.0.1:8000")
    assert not is_localhost("http://google.com")


def test_host_resolution() -> None:
    """Host resolution behaves as expected."""
    i = ["http://localhost:8000"]
    e = ["http://localhost:8000", "http://127.0.0.1:8000"]

    o = resolve_hosts(i)
    assert equal(o, e)


def equal(a: List[str], b: List[str]) -> bool:
    """Test two lists for equality."""
    if len(a) != len(b):
        return False

    for item in a:
        if item not in b:
            return False

    for item in b:
        if item not in a:
            return False

    return True
