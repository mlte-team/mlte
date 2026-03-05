"""Fixtures for MLTE store unit tests."""

from contextlib import contextmanager
from unittest.mock import patch

import pytest
import sqlalchemy

from test.store.defaults import IN_MEMORY_SQLITE_DB


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
