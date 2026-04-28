"""Unit tests for export."""

from pathlib import Path
from typing import Callable

import pytest

from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.base import StoreType
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.constants import LOCAL_CATALOG_STORE_ID
from mlte.store.unified_store import UnifiedStore
from mlte.store.user.policy import user_policy
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import User
from test.store.catalog.conftest import get_test_entry_for_store
from test.store.conftest import create_test_unified_store
from test.store.export.conftest import ALL_EXPORT_SPEC
from test.store.user.test_underlying import get_internal_store_session, get_test_user, setup_test_group
from test.store.utils import store_types
from mlte.store.export.export import _export_catalogs, _export_custom_lists, _export_users


@pytest.mark.parametrize("store_type", store_types())
def test_export_custom_lists(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Test that custom lists can be exported."""
    stores: UnifiedStore = create_test_unified_store(store_type, tmp_path, patched_setup_stores)

    all_export = _export_custom_lists(ALL_EXPORT_SPEC, stores.custom_list_store)
    for name in CustomListName:
        assert name in all_export


@pytest.mark.parametrize("store_type", store_types())
def test_export_users(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Tests that users can be exported."""
    stores: UnifiedStore = create_test_unified_store(store_type, tmp_path, patched_setup_stores)
    test_user = get_test_user()

    with ManagedUserSession(stores.user_store.session()) as user_store_session:
        internal_store = get_internal_store_session(user_store_session, store_type)
        test_user = user_policy.set_default_user_policies(
            test_user, internal_store.policy_store
        )
        setup_test_group(user_store_session)
        user_store_session.user_mapper.create(test_user)

    export = _export_users(ALL_EXPORT_SPEC, stores.user_store)
    assert test_user.username in export
    assert test_user == User(**export[test_user.username])


@pytest.mark.parametrize("store_type", store_types())
def test_export_catalogs(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores
) -> None:
    """Tests that local catalog can be exported."""
    stores = create_test_unified_store(store_type, tmp_path, patched_setup_stores)
    test_entry = get_test_entry_for_store(store_type=store_type)

    with ManagedCatalogSession(stores.catalog_stores.catalogs[LOCAL_CATALOG_STORE_ID].session()) as local_catalog_store:
        local_catalog_store.entry_mapper.create(test_entry)

    export = _export_catalogs(stores.catalog_stores)
    assert test_entry.to_json() in export[LOCAL_CATALOG_STORE_ID]