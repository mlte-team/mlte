"""Fixtures for store export."""

from unittest.mock import patch

import pytest

from mlte.store.artifact.store import ArtifactStore
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.custom_list.store import CustomListStore
from mlte.store.export.export import ExportSpec, ALL_OPTION, _export
from mlte.store.user.store import UserStore


ALL_EXPORT_SPEC = ExportSpec(
    models=ALL_OPTION,
    custom_lists=ALL_OPTION,
    users=ALL_OPTION,
)

ARTIFACT_EXPORT_DATA = "artifact"
CUSTOM_LIST_EXPORT_DATA = "custom_list"
USER_EXPORT_DATA = "user"
CATALOG_EXPORT_DATA = "catalog"

@pytest.fixture
def patched_export():
    """Fixture to patch export functions."""

    def _export_artifacts_with_fixtures(export_spec: ExportSpec, artifact_store: ArtifactStore):
        return ARTIFACT_EXPORT_DATA
    
    def _export_custom_lists_with_fixtures(export_spec: ExportSpec, custom_list_store: CustomListStore):
        return CUSTOM_LIST_EXPORT_DATA
    
    def _export_users_with_fixtures(export_spec: ExportSpec, user_store: UserStore):
        return USER_EXPORT_DATA
    
    def _export_catalogs_with_fixtures(catalog_stores: CatalogStoreGroup):
        return CATALOG_EXPORT_DATA
    
    with patch(
        "mlte.store.export.export._export_artifacts",
        side_effect=_export_artifacts_with_fixtures
    ), patch(
        "mlte.store.export.export._export_custom_lists",
        side_effect=_export_custom_lists_with_fixtures
    ), patch(
        "mlte.store.export.export._export_users",
        side_effect=_export_users_with_fixtures
    ), patch(
        "mlte.store.export.export._export_catalogs",
        side_effect=_export_catalogs_with_fixtures
    ):
        yield _export