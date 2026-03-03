"""Base store export class."""

import json
from pathlib import Path

from mlte.session.session import session
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.user.store_session import ManagedUserSession




def library_export(export_spec: dict, output_path: Path) -> None:
    """
    Func to export when using the library, probably takes in a path to export to, and the structure of what to export

    :param export_spec: Selection of what items to be exported
    :param output_path: The path to write the export to
    """
    # Call export
    export_json = export(export_spec)

    # Write to output_path
    with open(output_path, "w") as output_file:
        json.dump(export_json, output_file, indent=4)


def export(export_spec: dict) -> None:
    """
    
    """
    # Define object to hold all JSON output
    export_dict = {
        "models": {},
        "custom_lists": {},
        "users": [],
        "default_test_catalog": [],
    }

    # Read items to be exported
    with ManagedArtifactSession(session().stores.artifact_store.session()) as artifact_store:
        for model_id in artifact_store.model_mapper.list():
            export_dict["models"][model_id] = {}
            for version_id in artifact_store.version_mapper.list(model_id):
                export_dict["models"][model_id][version_id] = {}
                for artifact_id in artifact_store.artifact_mapper.list((model_id, version_id)):
                    export_dict["models"][model_id][version_id][artifact_id] = artifact_store.artifact_mapper.read(artifact_id, (model_id, version_id)).to_json()
            
    with ManagedCustomListSession(session().stores.custom_list_store.session()) as custom_list_store:
        for custom_list_id in CustomListName:
            export_dict["custom_lists"][custom_list_id] = []
            for custom_list_entry in custom_list_store.custom_list_entry_mapper.list_details(custom_list_id):
                export_dict["custom_lists"][custom_list_id].append(custom_list_entry.to_json())

    # TODO: Handle permissions & groups
    with ManagedUserSession(session().stores.user_store.session()) as user_store:
        for user in user_store.user_mapper.list_details():
            export_dict["users"].append(user.to_json())

    with ManagedCatalogSession(session().stores.catalog_stores.catalogs["local"].session()) as catalog_store:
        for catalog_entry in catalog_store.entry_mapper.list_details():
            export_dict["default_test_catalog"].append(catalog_entry.to_json())

    return export_dict
