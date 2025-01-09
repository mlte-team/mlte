"""
mlte/store/custom_list/initial_custom_lists.py

MLTE initial custom lists to come with installation.
"""

from __future__ import annotations

import importlib.resources
import os
from typing import Optional
import json

from mlte.store import error
import mlte.store.custom_list.qa_categories as qa_category_entries
import mlte.store.custom_list.quality_attributes as quality_attribute_entries
from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import CustomListStoreSession, ManagedCustomListSession
from mlte.custom_list.model import CustomListEntry

class InitialCustomLists:
    """Initial lists populated with pre-defined quality attributes and QA categories."""

    DEFAULT_STORES_FOLDER = "stores"
    """Default root folder for all built-in stores."""

    @staticmethod
    def setup_initial_custom_lists(
        stores_uri: Optional[StoreURI] = None,
    ) -> CustomListStore:
        """
        Sets up the initial custom lists.

        :param store_uri: The URI of the store being used (i.e., base folder, base DB, etc).
        :return: The initial custom list store.
        """
        # Create the actual initial custom lists.
        print(f"Creating initial custom lists at URI: {stores_uri}")
        custom_list_store = create_custom_list_store(
            stores_uri.uri
        )

        with ManagedCustomListSession(custom_list_store.session()) as session:
            # Input all initial QA Category entries
            num_categories = 0
            qa_categories = importlib.resources.files(qa_category_entries)
            with importlib.resources.as_file(qa_categories) as qa_categories_path:
                with os.scandir(qa_categories_path) as files:
                    for file in files:
                        if file.is_file() and file.name.endswith("json"):
                            with open(file.path) as open_file:
                                entry = CustomListEntry(**json.load(open_file))
                                try:
                                    session.custom_list_entry_mapper.create("qa_categories", entry)
                                except error.ErrorAlreadyExists:
                                    # If default values are already there we dont want to overwrite any changes
                                    pass
                                num_categories += 1
            print(f"Loaded {num_categories} QA Categories for initial list")

            # Input all initial Quality Attribute entries
            num_attributes = 0
            quality_attributes = importlib.resources.files(quality_attribute_entries)
            with importlib.resources.as_file(quality_attributes) as quality_attributes_path:
                with os.scandir(quality_attributes_path) as files:
                    for file in files:
                        if file.is_file() and file.name.endswith("json"):
                            with open(file.path) as open_file:
                                entry = CustomListEntry(**json.load(open_file))
                                try: 
                                    session.custom_list_entry_mapper.create("quality_attributes", entry)
                                except error.ErrorAlreadyExists:
                                    # If default values are already there we dont want to overwrite any changes
                                    pass
                                num_attributes += 1
            print(f"Loaded {num_attributes} Quality Attributes for initial list")
            
        return custom_list_store