"""
mlte/store/custom_list/underyling/memory.py

Implementation of in-memory custom list store.
"""

from __future__ import annotations

from typing import Dict, List

import mlte.store.error as errors
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel, CustomListModel
from mlte.store.base import StoreURI
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import (
    CustomListEntryMapper,
    CustomListStoreSession,
)

# -----------------------------------------------------------------------------
# Memory Store
# -----------------------------------------------------------------------------


class InMemoryCustomListStore(CustomListStore):
    """An in-memory implementation of the MLTE custom list store."""

    def __init__(self, uri: StoreURI) -> None:
        self.storage = MemoryCustomListStorage()
        """The underlying storage for the store."""

        super().__init__(uri=uri)

    def session(self) -> InMemoryCustomListStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryCustomListStoreSession(storage=self.storage)

    def clone(self) -> InMemoryCustomListStore:
        """
        Clones the store. Shallow clone.
        :return: The cloned store
        """
        clone = InMemoryCustomListStore(self.uri)
        clone.storage.custom_lists = self.storage.custom_lists.copy()


class MemoryCustomListStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.custom_lists: Dict[CustomListName, Dict[str, CustomListEntryModel]] = {}


# -----------------------------------------------------------------------------
# InMemoryStoreSession
# -----------------------------------------------------------------------------


class InMemoryCustomListStoreSession(CustomListStoreSession):
    """An in-memory implementation of the MLTE custom list store."""

    def __init__(self, *, storage: MemoryCustomListStorage) -> None:
        self.custom_list_entry_mapper = InMemoryCustomListEntryMapper(
            storage=storage
        )
        """The mapper to the custom list entry CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing an in-memory session is a no-op.
        pass


class InMemoryCustomListEntryMapper(CustomListEntryMapper):
    """In-memory mapper for custom list entry resource"""

    def __init__(
        self,
        *,
        storage: MemoryCustomListStorage,
        entry_mapper: InMemoryCustomListEntryMapper,
    ) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.entry_mapper = entry_mapper
        """A reference to the entry mapper, to get updated entry info if needed."""

    def create(
        self,
        entry: CustomListEntryModel,
        list_name: CustomListName | None = None,
    ) -> CustomListEntryModel:
        self._check_custom_list_exists(list_name)
        if entry.name in self.storage.custom_lists[list_name]:
            raise errors.ErrorAlreadyExists(
                f"Custom List Entry {entry.name}"
            )

        self.storage.custom_lists[list_name][entry.name] = entry

    def edit(
        self,
        entry: CustomListEntryModel,
        list_name: CustomListName | None = None,
    ) -> CustomListEntryModel:
        self._check_custom_list_exists(list_name)
        if entry.name not in self.storage.custom_lists[list_name]:
            raise errors.ErrorNotFound(
                f"Custom List Entry {entry.name}"
            )

        self.storage.custom_lists[list_name][entry.name] = entry
        return entry

    def read(
        self, entry_name: str, list_name: CustomListName | None = None
    ) -> CustomListEntryModel:
        self._check_custom_list_exists(list_name)
        if entry_name.name not in self.storage.custom_lists[list_name]:
            raise errors.ErrorNotFound(f"Custom List Entry {entry_name}")

        entry = self.storage.custom_lists[list_name][entry_name]
        return entry
    
    def list(self, list_name: CustomListName | None = None) -> List[str]:
        self._check_custom_list_exists(list_name)
        return [entry_name for entry_name in self.storage.custom_lists[list_name].keys()]

    def delete(
        self, entry_name: str, list_name: CustomListName | None = None
    ) -> CustomListEntryModel:
        self._check_custom_list_exists(list_name)
        if entry_name.name not in self.storage.custom_lists[list_name]:
            raise errors.ErrorNotFound(f"Custom List Entry {entry_name}")
        
        popped = self.storage.custom_lists[list_name][entry_name]
        del self.storage.custom_lists[list_name][entry_name]
        return popped

    def _check_custom_list_exists(
        self, list_name: CustomListName | None
    ) -> None:
        """Checks if the custom lists exists within the store."""
        if list_name is None:
            raise ValueError("CustomListName cannot be None")
        elif list_name not in self.storage.custom_lists:
            raise ValueError(f"CustomListName, {list_name}, does not exist")
