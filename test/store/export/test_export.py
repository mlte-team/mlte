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
from mlte.store.constants import LOCAL_CATALOG_STORE_ID, SAMPLE_CATALOG_STORE_ID
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
from test.store.conftest import create_test_unified_store
from test.store.export.conftest import (
    ARTIFACT_EXPORT_DATA,
    CATALOG_EXPORT_DATA,
    CUSTOM_LIST_EXPORT_DATA,
    USER_EXPORT_DATA,
    create_all_export_spec,
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
    all_export_spec = create_all_export_spec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    export_to_file(
        all_export_spec,
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
def test_export(
    store_type: StoreType, tmp_path: Path, patched_setup_stores, patched_export
) -> None:
    """Tests that all exports happen together properly"""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    all_export_spec = create_all_export_spec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    export = _export(
        all_export_spec,
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

    all_export_spec = create_all_export_spec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    all_export = _export_artifacts(all_export_spec, stores.artifact_store)
    assert (
        written_artifact.header.identifier in all_export[model_id][version_id]
    )
    assert (
        written_artifact.to_json()
        == all_export[model_id][version_id][written_artifact.header.identifier]
    )

    partial_spec = ExportSpec(
        stores.artifact_store,
        stores.user_store,
        stores.catalog_stores,
        models={model_id: [version_id]},
    )
    partial_export = _export_artifacts(partial_spec, stores.artifact_store)
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

    none_spec = ExportSpec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    none_export = _export_artifacts(none_spec, stores.artifact_store)
    assert none_export == {}


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

    all_export_spec = create_all_export_spec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    all_export = _export_custom_lists(all_export_spec, stores.custom_list_store)
    for name in CustomListName:
        assert name in all_export

    partial_spec = ExportSpec(
        stores.artifact_store,
        stores.user_store,
        stores.catalog_stores,
        custom_lists=[CustomListName.TAGS],
    )
    partial_export = _export_custom_lists(
        partial_spec, stores.custom_list_store
    )
    assert CustomListName.TAGS in partial_export

    none_spec = ExportSpec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    none_export = _export_custom_lists(none_spec, stores.custom_list_store)
    assert none_export == {}


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

    all_export_spec = create_all_export_spec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    full_export = _export_users(all_export_spec, stores.user_store)
    assert test_user.username in full_export
    assert test_user == User(**full_export[test_user.username])

    partial_spec = ExportSpec(
        stores.artifact_store,
        stores.user_store,
        stores.catalog_stores,
        users=[test_user.username],
    )
    partial_export = _export_users(partial_spec, stores.user_store)
    assert test_user.username in partial_export
    assert test_user == User(**partial_export[test_user.username])

    none_spec = ExportSpec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    none_export = _export_users(none_spec, stores.user_store)
    assert none_export == {}


@pytest.mark.parametrize("store_type", store_types())
def test_export_catalogs(
    store_type: StoreType, tmp_path: Path, patched_setup_stores
) -> None:
    """Tests that local catalog can be exported."""
    stores: UnifiedStore = create_test_unified_store(
        store_type, tmp_path, patched_setup_stores
    )

    all_export_spec = create_all_export_spec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    full_export = _export_catalogs(all_export_spec, stores.catalog_stores)
    assert SAMPLE_CATALOG_STORE_ID in full_export
    assert LOCAL_CATALOG_STORE_ID in full_export

    partial_spec = ExportSpec(
        stores.artifact_store,
        stores.user_store,
        stores.catalog_stores,
        catalogs=[LOCAL_CATALOG_STORE_ID],
    )
    partial_export = _export_catalogs(partial_spec, stores.catalog_stores)
    assert SAMPLE_CATALOG_STORE_ID not in partial_export
    assert LOCAL_CATALOG_STORE_ID in partial_export

    none_spec = ExportSpec(
        stores.artifact_store, stores.user_store, stores.catalog_stores
    )
    none_export = _export_catalogs(none_spec, stores.catalog_stores)
    assert none_export == {}
