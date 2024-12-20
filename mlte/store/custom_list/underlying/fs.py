"""
mlte/store/custom_list/underlying/fs.py

Implementation of local file system custom list store.
"""
from __future__ import annotations

from pathlib import Path

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
# FileSystemCustomLilstStoreSession
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

    CUSTOM_LIST_FOLDER = "custom_lists"
    """Subfolder for custom lists."""

    def __init__(
        self, storage: FileSystemStorage
    ) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.storage.set_base_path(
            Path(FileSystemCustomListStore.BASE_CUSTOM_LIST_FOLDER, self.CUSTOM_LIST_FOLDER)
        )
        """Set the subfodler for this resource."""

    def create(self, custom_list: CustomList) -> CustomList:
        self.storage.ensure_resource_does_not_exist(custom_list.name)
        return self._write_entry(custom_list)
    
    def _write_entry(self, custom_list: CustomList) -> CustomList:
        """Writes a entry to storage."""
        self.storage.write_resource(custom_list.name, custom_list.model_dump())
        return self._read_entry(custom_list.name)


# -----------------------------------------------------------------------------
# FileSystemCustomListEntryMappper
# -----------------------------------------------------------------------------


class FileSystemCustomListEntryMapper(CustomListEntryMapper):
    pass