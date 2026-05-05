"""Fixtures for store export."""

from typing import Any
from unittest.mock import patch

import pytest

from mlte.store.artifact.store import ArtifactStore
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.custom_list.store import CustomListStore
from mlte.store.export.export import ExportSpec, _export
from mlte.store.user.store import UserStore

ARTIFACT_EXPORT_DATA: dict[str, Any] = {
    "testModel": {
        "0.0.1": {
            "evidence.test": {"header": {}, "body": {}},
        }
    }
}
CUSTOM_LIST_EXPORT_DATA: dict[str, Any] = {
    "testCustomList": [
        {
            "name": "test1",
            "description": "test1",
            "parent": None,
        }
    ]
}
USER_EXPORT_DATA: dict[str, Any] = {
    "testUser": {
        "username": "testUser",
    }
}
CATALOG_EXPORT_DATA: dict[str, Any] = {
    "testCatalog": [{"header": {"identifier": "testIdentifier"}, "tags": []}]
}


def create_all_export_spec(
    artifact_store: ArtifactStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
) -> ExportSpec:
    return ExportSpec(
        artifact_store, user_store, catalog_stores, {}, [], [], []
    )


@pytest.fixture
def patched_export():
    """Fixture to patch export functions."""

    def _export_artifacts_with_fixtures(
        export_spec: ExportSpec, artifact_store: ArtifactStore
    ):
        return ARTIFACT_EXPORT_DATA

    def _export_custom_lists_with_fixtures(
        export_spec: ExportSpec, custom_list_store: CustomListStore
    ):
        return CUSTOM_LIST_EXPORT_DATA

    def _export_users_with_fixtures(
        export_spec: ExportSpec, user_store: UserStore
    ):
        return USER_EXPORT_DATA

    def _export_catalogs_with_fixtures(
        export_spec: ExportSpec, catalog_stores: CatalogStoreGroup
    ):
        return CATALOG_EXPORT_DATA

    with patch(
        "mlte.store.export.export._export_artifacts",
        side_effect=_export_artifacts_with_fixtures,
    ), patch(
        "mlte.store.export.export._export_custom_lists",
        side_effect=_export_custom_lists_with_fixtures,
    ), patch(
        "mlte.store.export.export._export_users",
        side_effect=_export_users_with_fixtures,
    ), patch(
        "mlte.store.export.export._export_catalogs",
        side_effect=_export_catalogs_with_fixtures,
    ):
        yield _export
