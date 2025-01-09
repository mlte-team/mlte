"""
mlte/store/custom_list/underlying/fs.py

Implementation of local file system custom list store.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from mlte.custom_list.model import CustomList, CustomListEntry
from mlte.store.base import StoreURI
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import CustomListStoreSession, CustomListMapper, CustomListEntryMapper
from mlte.store.common.fs_storage import FileSystemStorage

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
        self.custom_list_mapper = FileSystemCustomListMapper(storage)
        """The mapper to custom list CRUD."""

        self.custom_list_entry_mapper = FileSystemCustomListEntryMapper(storage)
        """The mapper to custom list entry CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass


# -----------------------------------------------------------------------------
# FileSystemCustomListMappper
# -----------------------------------------------------------------------------


class FileSystemCustomListMapper(CustomListMapper):
    """FS mapper for the custom list resource."""

    def __init__(
        self, storage: FileSystemStorage
    ) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.storage.set_base_path(
            Path(FileSystemCustomListStore.BASE_CUSTOM_LIST_FOLDER)
        )
        """Set the subfolder for this resource."""

    def create(self, custom_list: CustomList) -> CustomList:
        self.storage.ensure_resource_does_not_exist(custom_list.name)
        return self._write_list(custom_list)
    
    def edit(self, custom_list: CustomList) -> CustomList:
        self.storage.ensure_resource_exists(custom_list.name)
        return self._write_list(custom_list)
    
    def read(self, list_name: str) -> CustomList:
        return self._read_list(list_name)
    
    def list(self) -> List[str]:
        return self.storage.list_resources()
    
    def delete(self, list_name: str) -> CustomList:
        self.storage.ensure_resource_exists(list_name)
        custom_list = self._read_list(list_name)
        self.storage.delete_resource(list_name)
        return custom_list
    
    def _read_list(self, name: str) -> CustomList:
        """Reads a custom list."""
        self.storage.ensure_resource_exists(name)
        return CustomList(**self.storage.read_resource(name))
    
    def _write_list(self, custom_list: CustomList) -> CustomList:
        """Writes a custom list to storage."""
        self.storage.write_resource(custom_list.name, custom_list.model_dump())
        return self._read_list(custom_list.name)


# -----------------------------------------------------------------------------
# FileSystemCustomListEntryMappper
# -----------------------------------------------------------------------------


class FileSystemCustomListEntryMapper(CustomListEntryMapper):
    """FS mapper for the custom list entry resource."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""
    
    def create(self, custom_list_name: str, custom_list_entry: CustomListEntry) -> CustomListEntry:
        self._set_base_path(custom_list_name)
        self.storage.ensure_resource_does_not_exist(custom_list_entry.name)
        return self._write_entry(custom_list_entry)

    def edit(self, custom_list_name: str, custom_list_entry: CustomListEntry) -> CustomListEntry:
        self._set_base_path(custom_list_name)
        self.storage.ensure_resource_exists(custom_list_entry.name)
        return self._write_entry(custom_list_entry)

    def read(self, custom_list_name: str, entry_name: str) -> CustomListEntry:
        self._set_base_path(custom_list_name)
        return self._read_entry(entry_name)
    
    def list(self, custom_list_name: str) -> List[str]:
        self._set_base_path(custom_list_name)
        return self.storage.list_resources()
    
    def delete(self, custom_list_name: str, entry_name: str) -> CustomListEntry:
        self._set_base_path(custom_list_name)
        self.storage.ensure_resource_exists(entry_name)
        entry = self._read_list(entry_name)
        self.storage.delete_resource(entry_name)
        return entry

    def _read_entry(self, entry_name: str) -> CustomListEntry:
        """Reads a custom list entry."""
        self.storage.ensure_resource_exists(entry_name)
        return CustomListEntry(**self.storage.read_resource(entry_name))

    def _write_entry(self, entry: CustomListEntry) -> CustomListEntry:
        """Writes a custom list entry to storage."""
        self.storage.write_resource(entry.name, entry.model_dump())
        return self._read_entry(entry.name)

    def _set_base_path(self, custom_list_name: str) -> None:
        if custom_list_name in CustomListStore.CustomListNames._value2member_map_:
            self.storage.set_base_path(
                Path(self.storage.sub_folder, custom_list_name)
            )
        else:
            print("Invalid custom list name")
            # TODO : Handle this case
