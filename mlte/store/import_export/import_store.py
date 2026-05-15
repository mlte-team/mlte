
from typing import Any

from mlte.artifact.model import ArtifactModel
from mlte.catalog.model import CatalogEntry
from mlte.context.model import Model, Version
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store import error
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
from mlte.user.model import UserWithPassword


def import_store(
    store_data: dict[str, Any],
    artifact_store: ArtifactStore,
    custom_list_store: CustomListStore,
    user_store: UserStore,
    catalog_stores: CatalogStoreGroup,
    force: bool = False,
) -> None:
    """
    Import MLTE store objects from json dict.
    """
    if MODELS_KEY in store_data:
        _import_artifacts(store_data[MODELS_KEY], artifact_store, force)
    if CUSTOM_LISTS_KEY in store_data:
        _import_custom_lists(store_data[CUSTOM_LISTS_KEY], custom_list_store, force)
    if USERS_KEY in store_data:
        _import_users(store_data[USERS_KEY], user_store, force)
    if CATALOG_KEY in store_data:
        _import_catalogs(store_data[CATALOG_KEY], catalog_stores, force)


def _import_artifacts(
    artifact_data: dict[str, Any],
    artifact_store: ArtifactStore,
    force: bool = False
) -> None:
    """"""
    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        model_id_list = artifact_store_session.model_mapper.list()

        # This probably shouldn't error if the model_id is found, bc you would want to be able to mport into a model?
        for model_id in artifact_data.keys():
            if model_id not in model_id_list:
                artifact_store_session.model_mapper.create(Model(identifier=model_id))
            elif model_id in model_id_list and force:
                pass
            elif model_id in model_id_list and not force:
                raise error.ErrorAlreadyExists(f"Model {model_id}")
    
            version_id_list = artifact_store_session.version_mapper.list(model_id)

            for version_id in artifact_data[model_id].keys():
                if version_id not in version_id_list:
                    artifact_store_session.version_mapper.create(Version(identifier=version_id), model_id)
                elif version_id in version_id_list and force:
                    pass
                elif version_id in version_id_list and not force:
                    raise error.ErrorAlreadyExists(f"Version {version_id} in model {model_id}")
            
                artifact_id_list = artifact_store_session.artifact_mapper.list((model_id, version_id))

                for artifact_id in artifact_data[model_id][version_id].keys():
                    if artifact_id not in artifact_id_list:
                        artifact_store_session.artifact_mapper.create(ArtifactModel(**artifact_data[model_id][version_id][artifact_id]), (model_id, version_id))



def _import_custom_lists(
    custom_list_data: dict[str, Any],
    custom_list_store: CustomListStore,
    force: bool = False
) -> None:
    """"""
    with ManagedCustomListSession(custom_list_store.session()) as custom_list_store_session:
        for list_name in custom_list_data.keys():
            if list_name not in list(map(str, CustomListName)):
                raise error.ErrorNotFound(f"CustomListName {list_name} does not exist.")
            else:
                list_name = CustomListName(list_name)

            entry_id_list = custom_list_store_session.custom_list_entry_mapper.list(list_name)

            for entry in custom_list_data[list_name]:
                if entry["name"] not in entry_id_list:
                    custom_list_store_session.custom_list_entry_mapper.create(CustomListEntryModel(**entry), list_name)
                elif entry["name"] in entry_id_list and not force:
                    raise error.ErrorAlreadyExists(f"Entry {entry['name']} in Custom List {list_name}")
                elif entry["name"] in entry_id_list and force:
                    custom_list_store_session.custom_list_entry_mapper.edit(CustomListEntryModel(**entry), list_name)


def _import_users(
    user_data: dict[str, Any],
    user_store: UserStore,
    force: bool = False
) -> None:
    """"""
    with ManagedUserSession(user_store.session()) as user_store_session:
        user_name_list = user_store_session.user_mapper.list()

        # how do we go from a "User" that has the hashed password that we are importing, to "UserWithPassword" that expects plain text passowrd?

        for user_name in user_data.keys():
            if user_name not in user_name_list:
                user_store_session.user_mapper.create(UserWithPassword(**user_data[user_name]))
            elif user_name in user_name_list and not force:
                raise error.ErrorAlreadyExists(f"User {user_name}")
            elif user_name in user_name_list and force:
                user_store_session.user_mapper.edit(UserWithPassword(**user_data[user_name]))


def _import_catalogs(
    catalog_data: dict[str, Any],
    catalog_stores: CatalogStoreGroup,
    force: bool = False
) -> None:
    """"""
    for catalog_name in catalog_data.keys():
        with ManagedCatalogSession(catalog_stores.catalogs[catalog_name].session()) as catalog_store_session:
            entry_list = catalog_store_session.entry_mapper.list()

            for entry in catalog_data[catalog_name]:
                entry_id = entry["header"]["identifier"]
                if entry_id not in entry_list:
                    catalog_store_session.entry_mapper.create(CatalogEntry(**entry))
                elif entry_id in entry_list and not force:
                    raise error.ErrorAlreadyExists(f"Entry {entry_id} in catalog {catalog_name}")
                elif entry_id in entry_list and force:
                    catalog_store_session.entry_mapper.edit(CatalogEntry(**entry))