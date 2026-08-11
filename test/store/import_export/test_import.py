from pathlib import Path

import pytest

import mlte.store.error as errors
from mlte.artifact.type import ArtifactType
from mlte.catalog.model import CatalogEntry
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.base import StoreType
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.import_export.import_store import (
    _import_artifacts,
    _import_catalogs,
    _import_custom_lists,
    _import_users,
    import_store,
)
from mlte.store.unified_store import UnifiedStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import User
from test.fixture.artifact import ArtifactModelFactory
from test.store.conftest import create_test_unified_store
from test.store.import_export.conftest import (
    ALL_EXPORT_DATA,
    CATALOG_EXPORT_DATA,
    CUSTOM_LIST_EXPORT_DATA,
    USER_EXPORT_DATA,
)
from test.store.utils import store_types


@pytest.mark.parametrize("store_type", list(store_types()))
def test_import(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Tests that all import happen together properly."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    import_store(
        ALL_EXPORT_DATA,
        stores.artifact_store,
        stores.custom_list_store,
        stores.user_store,
        stores.catalog_stores,
    )

    with pytest.raises(errors.ErrorAlreadyExists):
        import_store(
            ALL_EXPORT_DATA,
            stores.artifact_store,
            stores.custom_list_store,
            stores.user_store,
            stores.catalog_stores,
        )

    import_store(
        ALL_EXPORT_DATA,
        stores.artifact_store,
        stores.custom_list_store,
        stores.user_store,
        stores.catalog_stores,
        True,
    )


@pytest.mark.parametrize("store_type", list(store_types()))
def test_import_artifacts(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Tests that artifacts can be imported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"
    artifact_type = ArtifactType.NEGOTIATION_CARD
    artifact = ArtifactModelFactory.make(artifact_type, artifact_id)
    import_data = {model_id: {version_id: {artifact_id: artifact.to_json()}}}

    _import_artifacts(import_data, stores.artifact_store)

    with ManagedArtifactSession(
        stores.artifact_store.session()
    ) as artifact_store_session:
        assert artifact == artifact_store_session.artifact_mapper.read(
            f"card.{artifact_id}", (model_id, version_id)
        )


@pytest.mark.parametrize("store_type", list(store_types()))
def test_import_custom_lists(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Test that custom lists can be imported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )
    list_name = CustomListName(list(CUSTOM_LIST_EXPORT_DATA)[0])
    entry = CUSTOM_LIST_EXPORT_DATA[list_name.value][0]

    _import_custom_lists(CUSTOM_LIST_EXPORT_DATA, stores.custom_list_store)

    with ManagedCustomListSession(
        stores.custom_list_store.session()
    ) as custom_list_store_session:
        assert CustomListEntryModel(
            **entry
        ) == custom_list_store_session.custom_list_entry_mapper.read(
            entry["name"], list_name
        )


@pytest.mark.parametrize("store_type", list(store_types()))
def test_import_users(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Test that users can be imported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )
    username = list(USER_EXPORT_DATA)[0]
    user = USER_EXPORT_DATA[username]

    _import_users(USER_EXPORT_DATA, stores.user_store)

    with ManagedUserSession(stores.user_store.session()) as user_store_session:
        # TODO: In the future we should also probably check permissions
        assert User(**user) == user_store_session.user_mapper.read(username)


@pytest.mark.parametrize("store_type", list(store_types()))
def test_import_catalogs(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Test that catalogs can be imported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )
    catalog_name = list(CATALOG_EXPORT_DATA)[0]
    entry = CATALOG_EXPORT_DATA[catalog_name][0]

    _import_catalogs(CATALOG_EXPORT_DATA, stores.catalog_stores)

    with ManagedCatalogSession(
        stores.catalog_stores.catalogs[catalog_name].session()
    ) as catalog_store_session:
        assert CatalogEntry(**entry) == catalog_store_session.entry_mapper.read(
            entry["header"]["identifier"]
        )
