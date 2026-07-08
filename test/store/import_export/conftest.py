"""Fixtures for store export."""

from typing import Any
from unittest.mock import patch

import pytest

from mlte.store.artifact.store import ArtifactStore
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.custom_list.store import CustomListStore
from mlte.store.import_export.constants import CATALOG_KEY, CUSTOM_LISTS_KEY, MODELS_KEY, USERS_KEY
from mlte.store.import_export.export_store import ExportSpec, _export
from mlte.store.user.store import UserStore

ARTIFACT_EXPORT_DATA: dict[str, Any] = {
    "testModel": {
        "0.0.1": {
            "evidence.accuracy across gardens": {
            "header": {
                "identifier": "evidence.accuracy across gardens",
                "type": "evidence",
                "timestamp": 1770690184,
                "creator": None,
                "level": "version"
            },
            "body": {
                "artifact_type": "evidence",
                "metadata": {
                    "test_case_id": "accuracy across gardens",
                    "measurement": {
                        "measurement_class": "mlte.measurement.external_measurement.ExternalMeasurement",
                        "output_class": "mlte.evidence.types.array.Array",
                        "additional_data": {
                            "function": "__main__.calculate_model_performance_acc"
                        }
                    }
                },
                "evidence_class": "mlte.evidence.types.array.Array",
                "value": {
                    "evidence_type": "array",
                    "data": [
                        0.981,
                        0.948,
                        0.961
                    ]
                }
            }
        },
        }
    }
}
CUSTOM_LIST_EXPORT_DATA: dict[str, Any] = {
    "classification": [
        {
            "name": "test1",
            "description": "test1",
            "parent": None,
        }
    ]
}
USER_EXPORT_DATA: dict[str, Any] = {
    "test": {
        "username": "test",
        "email": None,
        "full_name": None,
        "disabled": False,
        "role": "admin",
        "groups": [],
        "hashed_password": "$2b$12$SO4mZpM8utStmh5VABacZOVQgfrzI2/aD.pszSuJYf1gypt/oo2tG"
    },
}
CATALOG_EXPORT_DATA: dict[str, Any] = {
    "local": [
        {
            "header": {
                "identifier": "example",
                "creator": "admin",
                "created": 1763499421,
                "updater": None,
                "updated": 1763499421,
                "catalog_id": "local"
            },
            "tags": [
                "Computer Vision",
                "Image"
            ],
            "quality_attribute": "Analyzability",
            "code": "blah",
            "description": "Check that log enteries are produced for all OOD inputs",
            "inputs": "The model log path",
            "output": "Model logs; if OOD inputs are logged"
        }
    ]
}
ALL_EXPORT_DATA: dict[str, Any] = {
    MODELS_KEY: ARTIFACT_EXPORT_DATA,
    CUSTOM_LISTS_KEY: CUSTOM_LIST_EXPORT_DATA,
    USERS_KEY: USER_EXPORT_DATA,
    CATALOG_KEY: CATALOG_EXPORT_DATA,
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
        "mlte.store.import_export.export._export_artifacts",
        side_effect=_export_artifacts_with_fixtures,
    ), patch(
        "mlte.store.import_export.export._export_custom_lists",
        side_effect=_export_custom_lists_with_fixtures,
    ), patch(
        "mlte.store.import_export.export._export_users",
        side_effect=_export_users_with_fixtures,
    ), patch(
        "mlte.store.import_export.export._export_catalogs",
        side_effect=_export_catalogs_with_fixtures,
    ):
        yield _export
