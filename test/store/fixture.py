"""Fixtures for MLTE store unit tests."""

from contextlib import contextmanager
from typing import Generator
from unittest.mock import patch

import pytest
import sqlalchemy

from mlte.store.base import StoreType
from test.store.defaults import IN_MEMORY_SQLITE_DB


def store_types() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in StoreType:
        yield store_fixture_name.value


@pytest.fixture(scope="function")
def shared_sqlite_engine():
    """Opens a connection to a shared in-memory DB and keeps it alive."""
    engine = sqlalchemy.create_engine(IN_MEMORY_SQLITE_DB)
    temp_engine_dispose = engine.dispose
    engine.dispose = lambda: None  # type: ignore
    yield engine
    temp_engine_dispose()


@pytest.fixture(scope="function")
def patched_create_engine(shared_sqlite_engine):
    @contextmanager
    def _patched_create_engine_context():
        with patch(
            "mlte.store.common.rdbs_storage.sqlalchemy.create_engine"
        ) as mock_create_engine:
            mock_create_engine.return_value = shared_sqlite_engine
            yield

    return _patched_create_engine_context
