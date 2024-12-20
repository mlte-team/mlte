"""
mlte/store/custom_list/store_session.py

MLTE custom list store interface implementation
"""
from __future__ import annotations

from typing import List

from mlte.store.base import ResourceMapper, StoreSession
from mlte.custom_list.model import CustomList, CustomListEntry

# -----------------------------------------------------------------------------
# CustomListStoreSession
# -----------------------------------------------------------------------------


class CustomListStoreSession(StoreSession):
    """The base class for all implementations of the MLTE custom list store session."""

    custom_list_mapper: CustomListMapper
    """Mapper for the custom list resource."""

    custom_list_entry_mapper: CustomListEntryMapper
    """Mapper for the custom list entry resource."""


class CustomListMapper(ResourceMapper):
    """An interface for mapping CRUD actions to custom lists."""

    def create(self, new_custom_list: CustomList) -> CustomList:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_custom_list: CustomList) -> CustomList:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, custom_list_name: str) -> CustomList:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, custom_list_name: str) -> CustomList:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class CustomListEntryMapper(ResourceMapper):
    """An interface for mapping CRUD actions to custom list entries."""

    def create(self, new_custom_list_entry: CustomListEntry) -> CustomListEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_custom_list_entry: CustomListEntry) -> CustomListEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, custom_list_entry_name: str) -> CustomListEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, custom_list_entry_name: str) -> CustomListEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)