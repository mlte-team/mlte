"""
test/context/test_context.py

Unit tests for MLTE session context.
"""

import pytest

from mlte.context import Context


def test_complete() -> None:
    c = Context()
    c.namespace = "ns"
    c.model = "model"
    c.version = "v0.0.1"
    c.uri = "http://localhost:8080"

    assert c.is_populated()
    c.assert_populated()


def test_missing_namespace() -> None:
    c = Context()
    c.model = "model"
    c.version = "v0.0.1"
    c.uri = "http://localhost:8080"

    assert not c.is_populated()

    with pytest.raises(RuntimeError):
        c.assert_populated()


def test_missing_model() -> None:
    c = Context()
    c.namespace = "ns"
    c.version = "v0.0.1"
    c.uri = "http://localhost:8080"

    assert not c.is_populated()

    with pytest.raises(RuntimeError):
        c.assert_populated()


def test_missing_version() -> None:
    c = Context()
    c.namespace = "ns"
    c.model = "model"
    c.uri = "http://localhost:8080"

    assert not c.is_populated()

    with pytest.raises(RuntimeError):
        c.assert_populated()


def test_missing_uri() -> None:
    c = Context()
    c.namespace = "ns"
    c.model = "model"
    c.version = "v0.0.1"

    assert not c.is_populated()

    with pytest.raises(RuntimeError):
        c.assert_populated()
