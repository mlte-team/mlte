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

    # We turn off the dispose method, so it can stay alive between different calls.
    temp_engine_dispose = engine.dispose
    engine.dispose = lambda: None  # type: ignore

    yield engine

    # We now manually call dispose, since at this points the test has completed.
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


# @pytest.fixture
# def patched_setup_stores():
#    with patch(
#        "mlte.store.user.factory.create_user_store",
#        return_value=create_test_user_store,
#    ):
#        with patch(
#            "mlte.store.custom_list.factory.create_custom_list_store",
#            return_value=create_test_custom_list_store,
#        ):
#            with patch(
#                "mlte.store.artifact.factory.create_artifact_store",
#                return_value=create_test_artifact_store,
#            ):
#                with patch(
#                    "mlte.store.catalog.store.factory.create_catalog_store",
#                    return_value=create_test_catalog_store,
#                ):
#                    yield setup_stores
