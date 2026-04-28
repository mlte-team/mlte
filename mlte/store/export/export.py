"""Base store export class."""

import json
import os
import zipfile
from pathlib import Path
from typing import Any

from mlte.custom_list.custom_list_names import CustomListName
from mlte.model.base_model import BaseModel
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.constants import LOCAL_CATALOG_STORE_ID
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession

MODELS_KEY = "models"
CUSTOM_LISTS_KEY = "custom_lists"
USERS_KEY = "users"
CATALOG_KEY = "local_test_catalog"
EXPORT_ZIP_FILE = "store_export.zip"
EXPORT_JSON_FILE = "store_export.json"


class ExportSpec(BaseModel):
    """Specification of MLTE store objects to be exported."""

    models: dict[str, list[str]] | None = None
    """Dict of models to be exported. Key is model ID, value is list of versions."""

    custom_lists: list[CustomListName] | None = None
    """List of custom lists to be exported."""

    users: list[str] | None = None
    """List of user IDs for users to be exported."""


def export_to_file(
    export_spec: ExportSpec,
    output_path: Path,
    artifact_store: ArtifactStore,
    custom_list_store: CustomListStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
) -> None:
    """
    Export store data, writes the exported JSON to output_path as zip file.

    :param export_spec: Selection of MLTE store objects to be exported
    :param output_path: Path to write zipped JSON to
    """
    export_json = _export(
        export_spec,
        artifact_store,
        custom_list_store,
        user_store,
        catalog_stores,
    )

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    with zipfile.ZipFile(
        os.path.join(output_path, EXPORT_ZIP_FILE), "w", zipfile.ZIP_DEFLATED
    ) as zip_export_file:
        zip_export_file.writestr(
            EXPORT_JSON_FILE, json.dumps(export_json, indent=4)
        )


def _export(
    export_spec: ExportSpec,
    artifact_store: ArtifactStore,
    custom_list_store: CustomListStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
) -> dict[str, Any]:
    """
    Export MLTE store objects as json dict.

    :param export_spec: Selection of MLTE store objects to be exported
    :returns JSON containing all MLTE store objects specified in export_spec:
    """
    # Define object to hold all JSON output
    export_dict: dict[str, Any] = {
        MODELS_KEY: {},
        CUSTOM_LISTS_KEY: {},
        USERS_KEY: {},
        CATALOG_KEY: {},
    }

    # Read items to be exported
    export_dict[MODELS_KEY] = _export_artifacts(export_spec, artifact_store)
    export_dict[CUSTOM_LISTS_KEY] = _export_custom_lists(
        export_spec, custom_list_store
    )
    export_dict[USERS_KEY] = _export_users(export_spec, user_store)
    export_dict[CATALOG_KEY] = _export_catalogs(catalog_stores)

    return export_dict


def _export_artifacts(
    export_spec: ExportSpec, artifact_store: ArtifactStore
) -> dict[str, Any]:
    """Return dict of artifacts specified in export_spec."""
    output_dict: dict[str, Any] = {}

    # TODO: When getting multiple versions, this exports the card under each version. Should not do that
    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        if export_spec.models is None:
            return output_dict

        if export_spec.models == {}:
            for model_id in artifact_store_session.model_mapper.list():
                export_spec.models[model_id] = []

        for model_id in export_spec.models:
            if export_spec.models[model_id] == []:
                export_spec.models[model_id] = (
                    artifact_store_session.version_mapper.list(model_id)
                )

            output_dict[model_id] = {}
            for version_id in export_spec.models[model_id]:
                output_dict[model_id][version_id] = {}
                for artifact_id in artifact_store_session.artifact_mapper.list(
                    (model_id, version_id)
                ):
                    output_dict[model_id][version_id][artifact_id] = (
                        artifact_store_session.artifact_mapper.read(
                            artifact_id, (model_id, version_id)
                        ).to_json()
                    )

    return output_dict


def _export_custom_lists(
    export_spec: ExportSpec, custom_list_store: CustomListStore
) -> dict[str, Any]:
    """Return dict of custom lists specified in export_spec."""
    output_dict: dict[str, Any] = {}

    with ManagedCustomListSession(
        custom_list_store.session()
    ) as custom_list_store_session:
        if export_spec.custom_lists is None:
            return output_dict

        if export_spec.custom_lists == []:
            for custom_list_id in CustomListName:
                export_spec.custom_lists.append(custom_list_id)

        for custom_list_id in export_spec.custom_lists:
            output_dict[custom_list_id] = []
            for (
                custom_list_entry
            ) in custom_list_store_session.custom_list_entry_mapper.list_details(
                custom_list_id
            ):
                output_dict[custom_list_id].append(custom_list_entry.to_json())

    return output_dict


def _export_users(
    export_spec: ExportSpec, user_store: UserStore
) -> dict[str, Any]:
    """Return list of users specified in export_spec."""
    output_dict: dict[str, Any] = {}

    # TODO: Handle permissions & groups
    with ManagedUserSession(user_store.session()) as user_store_session:
        if export_spec.users is None:
            return output_dict

        if export_spec.users == []:
            export_spec.users = user_store_session.user_mapper.list()

        for user in export_spec.users:
            output_dict[user] = user_store_session.user_mapper.read(
                user
            ).to_json()

    return output_dict


def _export_catalogs(catalog_stores: CatalogStoreGroup) -> dict[str, Any]:
    """Return the local test catalog."""
    output_dict: dict[str, Any] = {LOCAL_CATALOG_STORE_ID: []}

    with ManagedCatalogSession(
        catalog_stores.catalogs[LOCAL_CATALOG_STORE_ID].session()
    ) as catalog_store_session:
        for catalog_entry in catalog_store_session.entry_mapper.list_details():
            output_dict[LOCAL_CATALOG_STORE_ID].append(catalog_entry.to_json())

    return output_dict
