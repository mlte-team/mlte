"""Unit tests for global session store management."""

import pytest

from mlte.store.base import StoreType, StoreURI
from mlte.store.unified_store import UnifiedStore
from test.session.conftest import create_test_session_stores
from test.store.utils import store_types

# -------------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------------


def test_add_catalog_store_from_uri():
    cat_id = "catalog1"
    session_stores = UnifiedStore()
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
