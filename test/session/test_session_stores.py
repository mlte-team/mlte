"""Unit tests for global session store management."""

import pytest

from mlte.session.session_stores import SessionStores
from mlte.store.base import StoreType, StoreURI
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.utils import store_types

# -------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------


def create_test_session_stores(
    store_type: StoreType,
    tmp_path,
    patched_setup_stores,
    catalog_uris: dict[str, str] = {},
) -> SessionStores:
    """Creates appropriate test session stores."""
    # We can't test setup_stores with a REMOTE store, since this would require setting up the session stores,
    # and then the TestAPI sets up its own session stores to act as a backend; however, since only one
    # state session is supported, this tries to overwrite the previous set up and it would fail.
    # TODO: Isolate how TestAPI works so that this can be tested.
    if store_type == StoreType.REMOTE_HTTP:
        pytest.skip()

    uri_string = create_uri_string(store_type, tmp_path)
    session_stores: SessionStores = patched_setup_stores(
        uri_string, catalog_uris
    )

    return session_stores


def create_uri_string(store_type: StoreType, tmp_path) -> str:
    if store_type == StoreType.RELATIONAL_DB:
        uri_string = IN_MEMORY_SQLITE_DB
    else:
        uri_string = StoreURI.create_uri_string(
            store_type,
            tmp_path if store_type == StoreType.LOCAL_FILESYSTEM else "",
        )
    return uri_string


# -------------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------------


def test_add_catalog_store_from_uri():
    cat_id = "catalog1"
    session_stores = SessionStores()
    session_stores.add_catalog_store_from_uri(
        StoreURI.create_uri_string(StoreType.REMOTE_HTTP, "catalog1"), cat_id
    )
    assert cat_id in session_stores.catalog_stores.catalogs


@pytest.mark.parametrize("store_type", store_types())
def test_setup_stores(store_type: StoreType, tmp_path, patched_setup_stores):
    session_stores = create_test_session_stores(
        store_type, tmp_path, patched_setup_stores
    )

    assert session_stores.artifact_store is not None
    assert session_stores.custom_list_store is not None
    assert session_stores.user_store is not None
    assert session_stores.catalog_stores.catalogs != {}


@pytest.mark.parametrize("store_type", store_types())
def test_setup_stores_with_catalog_uris(
    store_type: StoreType, tmp_path, patched_setup_stores
):
    cat_id = "catalog1"
    catalog_uris = {
        cat_id: StoreURI.create_uri_string(StoreType.REMOTE_HTTP, "catalog1")
    }

    session_stores = create_test_session_stores(
        store_type, tmp_path, patched_setup_stores, catalog_uris
    )

    assert cat_id in session_stores.catalog_stores.catalogs


def test_setup_stores_with_invalid_catalog_uri(patched_setup_stores):
    catalog_uris = {"local": "test-uri-cat"}
    with pytest.raises(RuntimeError):
        patched_setup_stores("test-uri", catalog_uris)
