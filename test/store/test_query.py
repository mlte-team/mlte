"""
test/store/test_query.py

Unit tests for store query functionality.
"""

from mlte.store.common.query import AllFilter, NoneFilter


def test_all() -> None:
    """The all filter can be serialized and deserialized."""
    f = AllFilter()
    assert AllFilter(**f.model_dump()) == f


def test_none() -> None:
    """The all filter cna be serialized and deserialized."""
    f = NoneFilter()
    assert NoneFilter(**f.model_dump()) == f
