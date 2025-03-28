"""MLTE initial custom lists to come with installation."""

from __future__ import annotations

import mlte.store.custom_list.qa_categories as qa_category_entries
import mlte.store.custom_list.quality_attributes as quality_attribute_entries
from mlte._private.reflection import get_json_resources
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store import error
from mlte.store.base import StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession


class InitialCustomLists:
    """Initial lists populated with pre-defined quality attributes and QA categories."""

    DEFAULT_STORES_FOLDER = "stores"
    """Default root folder for all built-in stores."""

    @staticmethod
    def setup_custom_list_store(
        stores_uri: StoreURI,
    ) -> CustomListStore:
        """
        Sets up a custom list store with the initial custom lists.

        :param stores_uri: The URI of the store being used (i.e., base folder, base DB, etc).
        :return: A custom list store populated with the initial entries.
        """
        # Create the initial custom lists.
        print(f"Creating initial custom lists at URI: {stores_uri}")
        custom_list_store = create_custom_list_store(stores_uri.uri)

        with ManagedCustomListSession(custom_list_store.session()) as session:
            num_categories = 0
            for json_data in get_json_resources(qa_category_entries):
                entry = CustomListEntryModel(**json_data)
                try:
                    session.custom_list_entry_mapper.create(
                        entry, CustomListName.QA_CATEGORIES
                    )
                except error.ErrorAlreadyExists:
                    # If default values are already there we dont want to overwrite any changes
                    pass
                num_categories += 1
            print(f"Loaded {num_categories} QA Categories for initial list")

            # Input all initial Quality Attribute entries
            num_attributes = 0
            for json_data in get_json_resources(quality_attribute_entries):
                entry = CustomListEntryModel(**json_data)
                try:
                    session.custom_list_entry_mapper.create(
                        entry, CustomListName.QUALITY_ATTRIBUTES
                    )
                except error.ErrorAlreadyExists:
                    # If default values are already there we dont want to overwrite any changes
                    pass
                num_attributes += 1
            print(
                f"Loaded {num_attributes} Quality Attributes for initial list"
            )

        return custom_list_store
