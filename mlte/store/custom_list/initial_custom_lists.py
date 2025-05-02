"""MLTE initial custom lists to come with installation."""

from __future__ import annotations

import os
from types import ModuleType

import mlte.store.custom_list.qa_categories as qa_category_entries
import mlte.store.custom_list.quality_attributes as quality_attribute_entries
from mlte._private.reflection import get_json_resources
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store import error
from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import (
    CustomListStoreSession,
    ManagedCustomListSession,
)


class InitialCustomLists:
    """Initial lists populated with pre-defined quality attributes and QA categories."""

    @staticmethod
    def setup_custom_list_store(
        stores_uri: str,
    ) -> CustomListStore:
        """
        Sets up a custom list store with the initial custom lists.

        :param stores_uri: The URI of the store being used (i.e., base folder, base DB, etc).
        :return: A custom list store populated with the initial entries.
        """
        # Workaround to force FS if DB or HTTP is requested, as they are not supported yet.
        # TODO: Remove this check once RDBS and HTTP are implemented.
        parsed_uri = StoreURI.from_string(stores_uri)
        if (
            parsed_uri.type == StoreType.RELATIONAL_DB
            or parsed_uri.type == StoreType.REMOTE_HTTP
        ):
            # Creates a  file system URI using the default stores folder.
            parsed_uri = StoreURI.create_default_fs_uri()
            os.makedirs(f"{parsed_uri.path}", exist_ok=True)

        # Create the initial custom lists.
        print(f"Creating initial custom lists at URI: {stores_uri}")
        # TODO : After section above is removed with implementation of RDBS and HTTP, make this var stores_uri
        custom_list_store = create_custom_list_store(parsed_uri.uri)

        with ManagedCustomListSession(custom_list_store.session()) as session:
            # Load both QA categoties and QA as default lists.
            InitialCustomLists._load_resources_to_list(
                session, qa_category_entries, CustomListName.QA_CATEGORIES
            )
            InitialCustomLists._load_resources_to_list(
                session,
                quality_attribute_entries,
                CustomListName.QUALITY_ATTRIBUTES,
            )

        return custom_list_store

    @staticmethod
    def _load_resources_to_list(
        store_session: CustomListStoreSession,
        module: ModuleType,
        list_name: CustomListName,
    ):
        """
        Loads all JSON resources from the given module into the store for the given list.

        :param store_session: The CustomList store session to store things to.
        :param module: The module where the JSON resources with the entries are in.
        :param list_name: The CustomListName that the entries will be associated to.
        """
        num_entries = 0
        for json_data in get_json_resources(module):
            entry = CustomListEntryModel(**json_data)
            try:
                store_session.custom_list_entry_mapper.create(entry, list_name)
            except error.ErrorAlreadyExists:
                # If default values are already there we dont want to overwrite any changes
                pass
            num_entries += 1
        print(f"Loaded {num_entries} {list_name.value} for initial list")
