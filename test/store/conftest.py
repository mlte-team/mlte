"""Fixtures for MLTE store unit tests."""

from contextlib import contextmanager
from unittest.mock import patch

import pytest
import sqlalchemy

from mlte.store.base import StoreType, StoreURI
from mlte.store.unified_store import UnifiedStore, setup_stores
from test.store.artifact.conftest import _create_artifact_store
from test.store.catalog.conftest import _create_catalog_store
from test.store.custom_list.conftest import _create_custom_list_store
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.user.conftest import _create_user_store


@pytest.fixture
def shared_sqlite_engine():
    """Opens a connection to a shared in-memory DB and keeps it alive."""
    engine = sqlalchemy.create_engine(IN_MEMORY_SQLITE_DB)

    # We turn off the dispose method, so it can stay alive between different calls.
    temp_engine_dispose = engine.dispose
    engine.dispose = lambda: None  # type: ignore

    yield engine

    # We now manually call dispose, since at this points the test has completed.
    temp_engine_dispose()


@pytest.fixture
def patched_create_engine(shared_sqlite_engine):
    @contextmanager
    def _patched_create_engine_context():
        with patch(
            "mlte.store.common.rdbs_storage.sqlalchemy.create_engine"
        ) as mock_create_engine:
            mock_create_engine.return_value = shared_sqlite_engine
            yield

    return _patched_create_engine_context


@pytest.fixture
def patched_setup_stores(tmpdir_factory, patched_create_engine):
    """Fixture to patch store factories for setup_stores method."""

    def _create_user_store_with_fixtures(uri: StoreURI):
        return _create_user_store(uri, tmpdir_factory)

    def _create_custom_list_store_with_fixtures(uri: StoreURI):
        return _create_custom_list_store(uri, tmpdir_factory)

    def _create_artifact_store_with_fixtures(uri: StoreURI):
        return _create_artifact_store(uri, tmpdir_factory)

    def _create_catalog_store_with_fixtures(
        uri: StoreURI, catalog_uris: dict[str, StoreURI]
    ):
        return _create_catalog_store(uri, catalog_uris, tmpdir_factory)

    with patch(
        "mlte.store.user.factory.create_user_store",
        side_effect=_create_user_store_with_fixtures,
    ), patch(
        "mlte.store.custom_list.factory.create_custom_list_store",
        side_effect=_create_custom_list_store_with_fixtures,
    ), patch(
        "mlte.store.custom_list.initial_custom_lists.create_custom_list_store",
        side_effect=_create_custom_list_store_with_fixtures,
    ), patch(
        "mlte.store.artifact.factory.create_artifact_store",
        side_effect=_create_artifact_store_with_fixtures,
    ), patch(
        "mlte.store.catalog.factory.create_catalog_store",
        side_effect=_create_catalog_store_with_fixtures,
    ), patch(
        "mlte.store.catalog.sample_catalog.create_catalog_store",
        side_effect=_create_catalog_store_with_fixtures,
    ), patched_create_engine():
        yield setup_stores


def create_test_unified_store(
    store_type: StoreType,
    tmp_path,
    patched_setup_stores,
    catalog_uris: dict[str, StoreURI] = {},
) -> UnifiedStore:
    """Creates appropriate test session stores."""
    # We can't test setup_stores with a REMOTE store, since this would require setting up the session stores,
    # and then the TestAPI sets up its own session stores to act as a backend; however, since only one
    # state session is supported, this tries to overwrite the previous set up and it would fail.
    # TODO: Isolate how TestAPI works so that this can be tested.
    if store_type == StoreType.REMOTE_HTTP:
        pytest.skip()

    uri = StoreURI.from_type(
        store_type,
        tmp_path if store_type == StoreType.LOCAL_FILESYSTEM else "",
    )
    session_stores: UnifiedStore = patched_setup_stores(uri, catalog_uris)

    return session_stores
