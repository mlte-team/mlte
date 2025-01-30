"""
mlte/store/custom_list/store_session.py

MLTE custom list store interface implementation
"""
from __future__ import annotations

from typing import List, cast

from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.base import ManagedSession, ResourceMapper, StoreSession

# -----------------------------------------------------------------------------
# CustomListStoreSession
# -----------------------------------------------------------------------------


class CustomListStoreSession(StoreSession):
    """The base class for all implementations of the MLTE custom list store session."""

    custom_list_entry_mapper: CustomListEntryMapper
    """Mapper for the custom list entry resource."""


class ManagedCustomListSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> CustomListStoreSession:
        return cast(CustomListStoreSession, self.session)


class CustomListEntryMapper(ResourceMapper):
    """An interface for mapping CRUD actions to custom list entries."""

    def create(
        self,
        new_custom_list_entry: CustomListEntryModel,
        custom_list_name: CustomListName,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(
        self,
        updated_custom_list_entry: CustomListEntryModel,
        custom_list_name: CustomListName,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def read(
        self, custom_list_entry_name: str, custom_list_name: CustomListName
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def list(
        self,
        custom_list_name: CustomListName,
    ) -> List[str]:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(
        self, custom_list_entry_name: str, custom_list_name: CustomListName
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)
