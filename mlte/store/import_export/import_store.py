
from typing import Any

from mlte.artifact.model import ArtifactModel
from mlte.catalog.model import CatalogEntry
from mlte.context.model import Model, Version
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
import mlte.store.error as errors
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.import_export.constants import (
    CATALOG_KEY,
    CUSTOM_LISTS_KEY,
    MODELS_KEY,
    USERS_KEY,
)
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import User


def import_store(
    import_data: dict[str, Any],
    artifact_store: ArtifactStore,
    custom_list_store: CustomListStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
    force: bool = False,
) -> None:
    """
    Import MLTE store objects from json dict.
    """

    if not force:
        _store_check(import_data, artifact_store, custom_list_store, user_store, catalog_stores)

    if MODELS_KEY in import_data:
        _import_artifacts(import_data[MODELS_KEY], artifact_store, force)
    if CUSTOM_LISTS_KEY in import_data:
        _import_custom_lists(import_data[CUSTOM_LISTS_KEY], custom_list_store, force)
    if USERS_KEY in import_data:
        _import_users(import_data[USERS_KEY], user_store, force)
    if CATALOG_KEY in import_data:
        _import_catalogs(import_data[CATALOG_KEY], catalog_stores, force)


def _store_check(
    import_data: dict[str, Any],
    artifact_store: ArtifactStore,
    custom_list_store: CustomListStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
) -> None:
    """Check if any of the data to be imported is already in the store."""
    if MODELS_KEY in import_data:
        _artifact_check(import_data[MODELS_KEY], artifact_store)
    if CUSTOM_LISTS_KEY in import_data:
        _custom_list_check(import_data[CUSTOM_LISTS_KEY], custom_list_store)
    if USERS_KEY in import_data:
        _users_check(import_data[USERS_KEY], user_store)
    if CATALOG_KEY in import_data:
        _catalogs_check(import_data[CATALOG_KEY], catalog_stores)


def _artifact_check(
    artifact_data: dict[str, Any],
    artifact_store: ArtifactStore,
) -> None:
    """Check if any models to be imported are already in the store."""
    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        model_id_list = artifact_store_session.model_mapper.list()
        for model_id in artifact_data.keys():
            if model_id in model_id_list:
                raise errors.ErrorAlreadyExists(f"Model {model_id}")
            
            # This is not really needed, because we don't want to overwrite any model info
            #   and if we don't want to do that, we just need the model to not be there then
            #   we can write whatever we want
            # version_id_list = artifact_store_session.version_mapper.list(model_id)
            # for version_id in artifact_data[model_id].keys():
            #     if version_id in version_id_list:
            #         raise errors.ErrorAlreadyExists(f"Version {version_id} in model {model_id}")
                
            #     artifact_id_list = artifact_store_session.artifact_mapper.list((model_id, version_id))
            #     for artifact_id in artifact_data[model_id][version_id].keys():
            #         if artifact_id in artifact_id_list:
            #             raise errors.ErrorAlreadyExists(f"Aritfact {artifact_id} in version {version_id} in model {model_id}")


def _custom_list_check(
    custom_list_data: dict[str, Any],
    custom_list_store: CustomListStore,
) -> None:
    """Check if any custom list entries to be imported are already in the store."""
    with ManagedCustomListSession(custom_list_store.session()) as custom_list_store_session:
        for list_name in custom_list_data.keys():
            if list_name not in list(map(str, CustomListName)):
                raise errors.ErrorNotFound(f"CustomListName {list_name} does not exist.")
            
            list_name = CustomListName(list_name)
            entry_id_list = custom_list_store_session.custom_list_entry_mapper.list(list_name)
            for entry in custom_list_data[list_name]:
                if entry["name"] in entry_id_list:
                    raise errors.ErrorAlreadyExists(f"Entry {entry['name']} in Custom List {list_name}")


def _users_check(
    user_data: dict[str, Any],
    user_store: UserStore
) -> None:
    """Check if any users to be imported are already in the store."""
    with ManagedUserSession(user_store.session()) as user_store_session:
        user_name_list = user_store_session.user_mapper.list()
        for user_name in user_data.keys():
            if user_name in user_name_list:
                raise errors.ErrorAlreadyExists(f"User {user_name}")


def _catalogs_check(
    catalogs_data: dict[str, Any],
    catalog_stores: CatalogStoreGroup,
) -> None:
    """Check if any catalog entries to be imported are already in the store."""
    for catalog_name in catalogs_data.keys():
        with ManagedCatalogSession(catalog_stores.catalogs[catalog_name].session()) as catalog_store_session:
            entry_list = catalog_store_session.entry_mapper.list()
            for entry in catalogs_data[catalog_name]:
                entry_id = entry["header"]["identifier"]
                if entry_id in entry_list:
                    raise errors.ErrorAlreadyExists(f"Entry {entry_id} in catalog {catalog_name}")


def _import_artifacts(
    artifact_data: dict[str, Any],
    artifact_store: ArtifactStore,
    force: bool = False
) -> None:
    """Import artifact data into store."""
    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        model_id_list = artifact_store_session.model_mapper.list()

        for model_id in artifact_data.keys():
            if model_id not in model_id_list:
                artifact_store_session.model_mapper.create(Model(identifier=model_id))
            elif model_id in model_id_list and force:
                pass
    
            version_id_list = artifact_store_session.version_mapper.list(model_id)
            for version_id in artifact_data[model_id].keys():
                if version_id not in version_id_list:
                    artifact_store_session.version_mapper.create(Version(identifier=version_id), model_id)
                elif version_id in version_id_list and force:
                    pass
            
                artifact_id_list = artifact_store_session.artifact_mapper.list((model_id, version_id))
                for artifact_id in artifact_data[model_id][version_id].keys():
                    if artifact_id not in artifact_id_list:
                        artifact_store_session.artifact_mapper.create(ArtifactModel(**artifact_data[model_id][version_id][artifact_id]), (model_id, version_id))
                    if artifact_id in artifact_id_list and force:
                        artifact_store_session.artifact_mapper.edit(ArtifactModel(**artifact_data[model_id][version_id][artifact_id]), (model_id, version_id))
                    

def _import_custom_lists(
    custom_list_data: dict[str, Any],
    custom_list_store: CustomListStore,
    force: bool = False
) -> None:
    """Imoprt custom list data into store."""
    with ManagedCustomListSession(custom_list_store.session()) as custom_list_store_session:
        for list_name in custom_list_data.keys():
            list_name = CustomListName(list_name)
            entry_id_list = custom_list_store_session.custom_list_entry_mapper.list(list_name)
            for entry in custom_list_data[list_name]:
                if entry["name"] not in entry_id_list:
                    custom_list_store_session.custom_list_entry_mapper.create(CustomListEntryModel(**entry), list_name)
                elif entry["name"] in entry_id_list and force:
                    custom_list_store_session.custom_list_entry_mapper.edit(CustomListEntryModel(**entry), list_name)


def _import_users(
    user_data: dict[str, Any],
    user_store: UserStore,
    force: bool = False
) -> None:
    """Import user data into store."""
    with ManagedUserSession(user_store.session()) as user_store_session:
        user_name_list = user_store_session.user_mapper.list()

        # how do we go from a "User" that has the hashed password that we are importing, to "UserWithPassword" that expects plain text passowrd?
        for user_name in user_data.keys():
            if user_name not in user_name_list:
                user_store_session.user_mapper.create(User(**user_data[user_name]))
            elif user_name in user_name_list and force:
                user_store_session.user_mapper.edit(User(**user_data[user_name]))


def _import_catalogs(
    catalogs_data: dict[str, Any],
    catalog_stores: CatalogStoreGroup,
    force: bool = False
) -> None:
    """Import catalog data into store."""
    for catalog_name in catalogs_data.keys():
        with ManagedCatalogSession(catalog_stores.catalogs[catalog_name].session()) as catalog_store_session:
            entry_list = catalog_store_session.entry_mapper.list()

            for entry in catalogs_data[catalog_name]:
                entry_id = entry["header"]["identifier"]
                if entry_id not in entry_list:
                    catalog_store_session.entry_mapper.create(CatalogEntry(**entry))
                elif entry_id in entry_list and force:
                    catalog_store_session.entry_mapper.edit(CatalogEntry(**entry))
