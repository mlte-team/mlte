"""Loading common fixtures used in tests in this and child folders."""

import pytest

from mlte.store.base import StoreType, StoreURI
from mlte.store.unified_store import UnifiedStore
from test.store.conftest import (
    patched_create_engine,
    patched_setup_stores,
    shared_sqlite_engine,
)

__all__ = [
    "shared_sqlite_engine",
    "patched_create_engine",
    "patched_setup_stores",
]


def create_test_session_stores(
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
    session_stores: UnifiedStore = patched_setup_stores(
        uri, catalog_uris
    )

    return session_stores
