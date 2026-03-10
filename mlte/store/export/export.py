"""Base store export class."""

import json
import os
import zipfile
from pathlib import Path
from typing import Any, TypedDict

from mlte.custom_list.custom_list_names import CustomListName
from mlte.session.session import session
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.user.store_session import ManagedUserSession


class ExportSpec(TypedDict):
    """TypedDict used to select MLTE store objects to be exported."""

    models: dict[str, list[str]]
    """Dict of models to be exported. Key is model ID, value is list of versions."""

    custom_lists: list[CustomListName]
    """List of custom lists to be exported."""

    users: list[str]
    """List of user IDs for users to be exported."""


def library_export(export_spec: ExportSpec, output_path: Path) -> None:
    """
    Export when using the library, writes the exported JSON to output_path as zip file.

    :param export_spec: Selection of MLTE store objects to be exported
    :param output_path: Path to write zipped JSON to
    """
    export_json = export(export_spec)

    with zipfile.ZipFile(
        os.path.join(output_path, "store_export.zip"), "w", zipfile.ZIP_DEFLATED
    ) as zip_export_file:
        zip_export_file.writestr(
            "store_export.json", json.dumps(export_json, indent=4)
        )


def export(export_spec: ExportSpec) -> dict[str, Any]:
    """
    Export MLTE store objects as json dict.

    :param export_spec: Selection of MLTE store objects to be exported
    :returns JSON containing all MLTE store objects specified in export_spec:
    """
    # Define object to hold all JSON output
    export_dict: dict[str, Any] = {
        "models": {},
        "custom_lists": {},
        "users": [],
        "default_test_catalog": [],
    }

    # Read items to be exported
    with ManagedArtifactSession(
        session().stores.artifact_store.session()
    ) as artifact_store:
        if "models" in export_spec:
            for model_id in export_spec["models"]:
                export_dict["models"][model_id] = {}
                for version_id in export_spec["models"][model_id]:
                    export_dict["models"][model_id][version_id] = {}
                    for artifact_id in artifact_store.artifact_mapper.list(
                        (model_id, version_id)
                    ):
                        export_dict["models"][model_id][version_id][
                            artifact_id
                        ] = artifact_store.artifact_mapper.read(
                            artifact_id, (model_id, version_id)
                        ).to_json()

    with ManagedCustomListSession(
        session().stores.custom_list_store.session()
    ) as custom_list_store:
        # TODO: This requires the input to be things like `CustomListName.CLASSIFICATION` in the spec, consider if we want this
        if "custom_lists" in export_spec:
            for custom_list_id in export_spec["custom_lists"]:
                export_dict["custom_lists"][custom_list_id] = []
                for (
                    custom_list_entry
                ) in custom_list_store.custom_list_entry_mapper.list_details(
                    custom_list_id
                ):
                    export_dict["custom_lists"][custom_list_id].append(
                        custom_list_entry.to_json()
                    )

    # TODO: Handle permissions & groups
    with ManagedUserSession(
        session().stores.user_store.session()
    ) as user_store:
        if "users" in export_spec:
            for user in export_spec["users"]:
                export_dict["users"].append(
                    user_store.user_mapper.read(user).to_json()
                )

    with ManagedCatalogSession(
        session().stores.catalog_stores.catalogs["local"].session()
    ) as catalog_store:
        for catalog_entry in catalog_store.entry_mapper.list_details():
            export_dict["default_test_catalog"].append(catalog_entry.to_json())

    return export_dict
