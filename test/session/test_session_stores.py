"""Unit tests for global session store management."""

import pytest

from mlte.session.session_stores import SessionStores, setup_stores
from mlte.store.base import StoreType, StoreURI
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.fixture import (  # noqa
    patched_create_engine,
    shared_sqlite_engine,
)


def create_uri_string(uri_type: StoreType, tmp_path) -> str:
    if uri_type == StoreType.RELATIONAL_DB:
        uri_string = IN_MEMORY_SQLITE_DB
    else:
        uri_string = StoreURI.create_uri_string(
            uri_type, tmp_path if uri_type == StoreType.LOCAL_FILESYSTEM else ""
        )
    return uri_string


def test_add_catalog_store_from_uri():
    cat_id = "catalog1"
    session_stores = SessionStores()
    session_stores.add_catalog_store_from_uri(
        StoreURI.create_uri_string(StoreType.REMOTE_HTTP, "catalog1"), cat_id
    )
    assert cat_id in session_stores.catalog_stores.catalogs


@pytest.mark.parametrize("uri_type", [type for type in StoreType])
def test_setup_stores(
    uri_type: StoreType, tmp_path, patched_create_engine  # noqa
):
    uri_string = create_uri_string(uri_type, tmp_path)

    if uri_type == StoreType.RELATIONAL_DB:
        with patched_create_engine():
            session_stores = setup_stores(uri_string)
    else:
        session_stores = setup_stores(uri_string)

    assert session_stores.artifact_store is not None
    assert session_stores.custom_list_store is not None
    assert session_stores.user_store is not None
    assert session_stores.catalog_stores.catalogs != {}


@pytest.mark.parametrize("uri_type", [type for type in StoreType])
def test_setup_stores_with_catalog_uris(
    uri_type: StoreType, tmp_path, patched_create_engine  # noqa
):
    uri_string = create_uri_string(uri_type, tmp_path)
    cat_id = "catalog1"
    catalog_uris = {
        cat_id: StoreURI.create_uri_string(StoreType.REMOTE_HTTP, "catalog1")
    }

    if uri_type == StoreType.RELATIONAL_DB:
        with patched_create_engine():
            session_stores = setup_stores(uri_string, catalog_uris)
    else:
        session_stores = setup_stores(uri_string, catalog_uris)

    assert cat_id in session_stores.catalog_stores.catalogs


def test_setup_stores_with_invalid_catalog_uri():
    catalog_uris = {"local": "test-uri-cat"}
    with pytest.raises(RuntimeError):
        setup_stores("test-uri", catalog_uris)
