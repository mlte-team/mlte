"""Implementation of local file system custom list store."""

from __future__ import annotations

from typing import List, Optional

from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.base import StoreURI
from mlte.store.common.fs_storage import FileSystemStorage
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import (
    CustomListEntryMapper,
    CustomListStoreSession,
)

# -----------------------------------------------------------------------------
# FileSystemCustomListStore
# -----------------------------------------------------------------------------


class FileSystemCustomListStore(CustomListStore):
    """A local file system implementation of the MLTE custom list store."""

    BASE_CUSTOM_LIST_FOLDER = "custom_lists"
    """Base folder to store custom lists in."""

    def __init__(self, uri: StoreURI) -> None:
        self.storage = FileSystemStorage(
            uri=uri, sub_folder=self.BASE_CUSTOM_LIST_FOLDER
        )
        """Underlying storage."""

        # Initialize defaults.
        super().__init__(uri=uri)

    def session(self) -> FileSystemCustomListStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return FileSystemCustomListStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# FileSystemCustomListStoreSession
# -----------------------------------------------------------------------------


class FileSystemCustomListStoreSession(CustomListStoreSession):
    """A local file-system implementation of the MLTE custom list store."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.custom_list_entry_mapper = FileSystemCustomListEntryMapper(storage)
        """The mapper to custom list entry CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass


# -----------------------------------------------------------------------------
# FileSystemCustomListEntryMappper
# -----------------------------------------------------------------------------


class FileSystemCustomListEntryMapper(CustomListEntryMapper):
    """FS mapper for the custom list entry resource."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        # Create folders for existing CustomLists.
        for custom_list_type in CustomListName:
            try:
                self.storage.create_resource_group(custom_list_type.value)
            except FileExistsError:
                # If it already existed, we just ignore warning.
                pass

    def create(
        self,
        entry: CustomListEntryModel,
        list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")
        self._ensure_parent_exists(entry.parent, list_name)
        self.storage.ensure_resource_does_not_exist(
            entry.name, [list_name.value]
        )
        return self._write_entry(entry, list_name)

    def read(
        self, entry_name: str, list_name: Optional[CustomListName] = None
    ) -> CustomListEntryModel:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")
        return self._read_entry(entry_name, list_name)

    def list(self, list_name: Optional[CustomListName] = None) -> List[str]:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")
        return self.storage.list_resources([list_name.value])

    def edit(
        self,
        entry: CustomListEntryModel,
        list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")
        self._ensure_parent_exists(entry.parent, list_name)
        self.storage.ensure_resource_exists(entry.name, [list_name.value])
        return self._write_entry(entry, list_name)

    def delete(
        self, entry_name: str, list_name: Optional[CustomListName] = None
    ) -> CustomListEntryModel:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")
        self.storage.ensure_resource_exists(entry_name, [list_name.value])
        entry = self._read_entry(entry_name, list_name)
        self._delete_children(list_name, entry_name)

        self.storage.delete_resource(entry_name, [list_name.value])
        return entry

    def _read_entry(
        self, entry_name: str, list_name: CustomListName
    ) -> CustomListEntryModel:
        """Reads a custom list entry."""
        self.storage.ensure_resource_exists(entry_name, [list_name.value])
        return CustomListEntryModel(
            **self.storage.read_resource(entry_name, [list_name.value])
        )

    def _write_entry(
        self, entry: CustomListEntryModel, list_name: CustomListName
    ) -> CustomListEntryModel:
        """Writes a custom list entry to storage."""
        self.storage.write_resource(
            entry.name, entry.to_json(), [list_name.value]
        )
        return self._read_entry(entry.name, list_name)
