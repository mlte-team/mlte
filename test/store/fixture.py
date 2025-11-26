"""Fixtures for MLTE store unit tests."""

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
