"""Base store export class."""

import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Final, Literal

from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.import_export.constants import (
    CATALOG_KEY,
    CUSTOM_LISTS_KEY,
    EXPORT_JSON_FILE,
    EXPORT_ZIP_FILE,
    MODELS_KEY,
    USERS_KEY,
)
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession

EXPORT_WILDCARD: Final = "*"

ExportWildcard = Literal["*"]


class ExportSpec:
    """Specification of MLTE store objects to be exported."""

    models: dict[str, list[str]] | None = None
    """
    Dict of models to be exported. Key is model ID, value is list of versions.

    An empty dict will export all models, all versions. An empty list of versions will export all versions.
    """

    custom_lists: list[CustomListName] | None = None
    """
    List of custom lists to be exported.

    An empty list will export all custom lists.
    """

    users: list[str] | None = None
    """
    List of user IDs for users to be exported.

    An empty list will export all users.
    """

    catalogs: list[str] | None = None
    """
    List of catalogs to be exported.

    An empty list will export all catalogs.
    """

    def __init__(
        self,
        artifact_store: ArtifactStore,
        user_store: UserStore,
        catalog_stores: CatalogStoreGroup,
        models: dict[str, list[str] | ExportWildcard] | ExportWildcard,
        custom_lists: list[CustomListName] | ExportWildcard,
        users: list[str] | ExportWildcard,
        catalogs: list[str] | ExportWildcard,
    ) -> None:
        self.models = self._setup_artifacts(artifact_store, models)
        self.custom_lists = self._setup_custom_lists(custom_lists)
        self.users = self._setup_users(user_store, users)
        self.catalogs = self._setup_catalogs(catalog_stores, catalogs)

    def _setup_artifacts(
        self,
        artifact_store: ArtifactStore,
        models: dict[str, list[str] | ExportWildcard] | ExportWildcard,
    ) -> dict[str, list[str]]:
        """Setup artifact export, accounts for the all option."""
        resolved_models: dict[str, list[str]] = {}

        with ManagedArtifactSession(artifact_store.session()) as session:
            target_models: dict[str, list[str] | ExportWildcard]
            if models == EXPORT_WILDCARD:
                target_models = {
                    model_id: EXPORT_WILDCARD
                    for model_id in session.model_mapper.list_all()
                }
            else:
                target_models = models

            for model_id, versions in target_models.items():
                if versions == EXPORT_WILDCARD:
                    resolved_models[model_id] = session.version_mapper.list_all(
                        model_id
                    )
                else:
                    resolved_models[model_id] = versions

        return resolved_models

    def _setup_custom_lists(
        self, custom_lists: list[CustomListName] | ExportWildcard
    ) -> list[CustomListName]:
        """Setup custom list export, accounts for the all option."""
        if custom_lists == EXPORT_WILDCARD:
            return list(CustomListName)
        return custom_lists

    def _setup_users(
        self, user_store: UserStore, users: list[str] | ExportWildcard
    ) -> list[str]:
        """Setup user export, accounts for the all option."""
        if users == EXPORT_WILDCARD:
            with ManagedUserSession(user_store.session()) as session:
                return session.user_mapper.list_all()
        return users

    def _setup_catalogs(
        self,
        catalog_stores: CatalogStoreGroup,
        catalogs: list[str] | ExportWildcard,
    ) -> list[str]:
        """Setup catalog export, accounts for the all option."""
        if catalogs == EXPORT_WILDCARD:
            return list(catalog_stores.catalogs.keys())
        return catalogs


def export_to_file(
    export_spec: ExportSpec,
    artifact_store: ArtifactStore,
    custom_list_store: CustomListStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
    output_path: Path | None = None,
) -> Path:
    """
    Export store data, writes the exported JSON to output_path as zip file.

    :param export_spec: Selection of MLTE store objects to be exported
    :param output_path: Directory or file path to write zipped JSON to
    :returns: Path of the exported zip file
    """
    export_json = _export(
        export_spec,
        artifact_store,
        custom_list_store,
        user_store,
        catalog_stores,
    )


    if output_path is None:
        target_dir = Path(tempfile.mkdtemp())
        zip_file_path = target_dir / EXPORT_ZIP_FILE
    else:
        if output_path.is_dir() or not output_path.suffix:
            output_path.mkdir(parents=True, exist_ok=True)
            zip_file_path = output_path / EXPORT_ZIP_FILE
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            zip_file_path = output_path

    with zipfile.ZipFile(
        zip_file_path, "w", zipfile.ZIP_DEFLATED
    ) as zip_export_file:
        zip_export_file.writestr(
            EXPORT_JSON_FILE, json.dumps(export_json, indent=2)
        )

    return zip_file_path


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
    export_dict[CATALOG_KEY] = _export_catalogs(export_spec, catalog_stores)

    return export_dict


def _export_artifacts(
    export_spec: ExportSpec, artifact_store: ArtifactStore
) -> dict[str, Any]:
    """Return dict of artifacts specified in export_spec."""
    output_dict: dict[str, Any] = {}

    if export_spec.models is None:
        return output_dict

    # TODO: When getting multiple versions, this exports the card under each version. Will have to be handled
    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        for model_id in export_spec.models:
            output_dict[model_id] = {}
            for version_id in export_spec.models[model_id]:
                output_dict[model_id][version_id] = {}
                for (
                    artifact_id
                ) in artifact_store_session.artifact_mapper.list_all(
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

    if export_spec.custom_lists is None:
        return output_dict

    with ManagedCustomListSession(
        custom_list_store.session()
    ) as custom_list_store_session:
        for custom_list_id in export_spec.custom_lists:
            output_dict[custom_list_id] = []
            for custom_list_entry in (
                custom_list_store_session.custom_list_entry_mapper.list_details(
                    custom_list_id
                )
            ):
                output_dict[custom_list_id].append(custom_list_entry.to_json())

    return output_dict


def _export_users(
    export_spec: ExportSpec, user_store: UserStore
) -> dict[str, Any]:
    """Return list of users specified in export_spec."""
    output_dict: dict[str, Any] = {}

    if export_spec.users is None:
        return output_dict

    # TODO: Handle permissions & groups
    with ManagedUserSession(user_store.session()) as user_store_session:
        for user in export_spec.users:
            output_dict[user] = user_store_session.user_mapper.read(
                user
            ).to_json()

    return output_dict


def _export_catalogs(
    export_spec: ExportSpec, catalog_stores: CatalogStoreGroup
) -> dict[str, Any]:
    """Return the local test catalog."""
    output_dict: dict[str, Any] = {}

    if export_spec.catalogs is None:
        return output_dict

    for catalog_name in export_spec.catalogs:
        with ManagedCatalogSession(
            catalog_stores.catalogs[catalog_name].session()
        ) as catalog_store_session:
            output_dict[catalog_name] = []
            for (
                catalog_entry
            ) in catalog_store_session.entry_mapper.list_details():
                output_dict[catalog_name].append(catalog_entry.to_json())

    return output_dict
