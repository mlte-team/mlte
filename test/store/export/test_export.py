"""Unit tests for export."""

import json
import zipfile
from pathlib import Path

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.base import StoreType
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.constants import LOCAL_CATALOG_STORE_ID
from mlte.store.export.export import (
    CATALOG_KEY,
    CUSTOM_LISTS_KEY,
    EXPORT_JSON_FILE,
    EXPORT_ZIP_FILE,
    MODELS_KEY,
    USERS_KEY,
    ExportSpec,
    _export,
    _export_artifacts,
    _export_catalogs,
    _export_custom_lists,
    _export_users,
    export_to_file,
)
from mlte.store.unified_store import UnifiedStore
from mlte.store.user.policy import user_policy
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import User
from test.fixture.artifact import ArtifactModelFactory
from test.store.catalog.conftest import get_test_entry_for_store
from test.store.conftest import create_test_unified_store
from test.store.export.conftest import (
    ALL_EXPORT_SPEC,
    ARTIFACT_EXPORT_DATA,
    CATALOG_EXPORT_DATA,
    CUSTOM_LIST_EXPORT_DATA,
    USER_EXPORT_DATA,
)
from test.store.user.test_underlying import (
    get_internal_store_session,
    get_test_user,
    setup_test_group,
)
from test.store.utils import store_types


@pytest.mark.parametrize("store_type", store_types())
def test_export_to_file(
    store_type: StoreType, tmp_path: Path, patched_setup_stores, patched_export
) -> None:
    """Tests that export is written to file."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )
    output_dir = tmp_path / "export"
    zip_path = output_dir / EXPORT_ZIP_FILE

    export_to_file(
        ALL_EXPORT_SPEC,
        output_dir,
        stores.artifact_store,
        stores.custom_list_store,
        stores.user_store,
        stores.catalog_stores,
    )

    assert output_dir.exists()
    assert zip_path.exists()

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        assert EXPORT_JSON_FILE in zip_ref.namelist()

        with zip_ref.open(EXPORT_JSON_FILE) as json_file:
            export_json = json.load(json_file)

            assert export_json[MODELS_KEY] == ARTIFACT_EXPORT_DATA
            assert export_json[CUSTOM_LISTS_KEY] == CUSTOM_LIST_EXPORT_DATA
            assert export_json[USERS_KEY] == USER_EXPORT_DATA
            assert export_json[CATALOG_KEY] == CATALOG_EXPORT_DATA


@pytest.mark.parametrize("store_type", store_types())
def test_export_orchestration(
    store_type: StoreType, tmp_path: Path, patched_setup_stores, patched_export
) -> None:
    """Tests that all exports happen together properly"""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    export = _export(
        ALL_EXPORT_SPEC,
        stores.artifact_store,
        stores.custom_list_store,
        stores.user_store,
        stores.catalog_stores,
    )

    assert export[MODELS_KEY] == ARTIFACT_EXPORT_DATA
    assert export[CUSTOM_LISTS_KEY] == CUSTOM_LIST_EXPORT_DATA
    assert export[USERS_KEY] == USER_EXPORT_DATA
    assert export[CATALOG_KEY] == CATALOG_EXPORT_DATA


@pytest.mark.parametrize("store_type", store_types())
def test_export_artifacts(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Tests that artifacts can be exported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"
    artifact_type = ArtifactType.NEGOTIATION_CARD

    with ManagedArtifactSession(
        stores.artifact_store.session()
    ) as artifact_store_session:
        artifact_store_session.model_mapper.create(Model(identifier=model_id))
        artifact_store_session.version_mapper.create(
            Version(identifier=version_id), model_id
        )

        artifact = ArtifactModelFactory.make(artifact_type, artifact_id)
        written_artifact = (
            artifact_store_session.artifact_mapper.write_artifact(
                model_id, version_id, artifact
            )
        )

    all_export = _export_artifacts(ALL_EXPORT_SPEC, stores.artifact_store)
    assert (
        written_artifact.header.identifier in all_export[model_id][version_id]
    )
    assert (
        written_artifact.to_json()
        == all_export[model_id][version_id][written_artifact.header.identifier]
    )

    test_spec = ExportSpec(models={model_id: [version_id]})
    partial_export = _export_artifacts(test_spec, stores.artifact_store)
    assert (
        written_artifact.header.identifier
        in partial_export[model_id][version_id]
    )
    assert (
        written_artifact.to_json()
        == partial_export[model_id][version_id][
            written_artifact.header.identifier
        ]
    )


@pytest.mark.parametrize("store_type", store_types())
def test_export_custom_lists(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Test that custom lists can be exported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    all_export = _export_custom_lists(ALL_EXPORT_SPEC, stores.custom_list_store)
    for name in CustomListName:
        assert name in all_export

    test_spec = ExportSpec(custom_lists=[CustomListName.TAGS])
    partial_export = _export_custom_lists(test_spec, stores.custom_list_store)
    assert CustomListName.TAGS in partial_export


@pytest.mark.parametrize("store_type", store_types())
def test_export_users(
    store_type: StoreType,
    tmp_path: Path,
    patched_setup_stores,
) -> None:
    """Tests that users can be exported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )
    test_user = get_test_user()

    with ManagedUserSession(stores.user_store.session()) as user_store_session:
        internal_store = get_internal_store_session(
            user_store_session, store_type
        )
        test_user = user_policy.set_default_user_policies(
            test_user, internal_store.policy_store
        )
        setup_test_group(user_store_session)
        user_store_session.user_mapper.create(test_user)

    full_export = _export_users(ALL_EXPORT_SPEC, stores.user_store)
    assert test_user.username in full_export
    assert test_user == User(**full_export[test_user.username])

    test_spec = ExportSpec(users=[test_user.username])
    partial_export = _export_users(test_spec, stores.user_store)
    assert test_user.username in partial_export
    assert test_user == User(**partial_export[test_user.username])


@pytest.mark.parametrize("store_type", store_types())
def test_export_catalogs(
    store_type: StoreType, tmp_path: Path, patched_setup_stores
) -> None:
    """Tests that local catalog can be exported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )
    test_entry = get_test_entry_for_store(store_type=store_type)

    with ManagedCatalogSession(
        stores.catalog_stores.catalogs[LOCAL_CATALOG_STORE_ID].session()
    ) as local_catalog_store:
        local_catalog_store.entry_mapper.create(test_entry)

    export = _export_catalogs(stores.catalog_stores)
    assert test_entry.to_json() in export[LOCAL_CATALOG_STORE_ID]
