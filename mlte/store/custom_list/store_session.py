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


# TODO : Have this inherit from ResourceMapper and figure out how to handle the mismatch in params
class CustomListEntryMapper:
    """An interface for mapping CRUD actions to custom list entries."""

    def create(
        self,
        custom_list_name: CustomListName,
        new_custom_list_entry: CustomListEntryModel,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(
        self,
        custom_list_name: CustomListName,
        updated_custom_list_entry: CustomListEntryModel,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def read(
        self, custom_list_name: CustomListName, custom_list_entry_name: str
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def list(
        self,
        custom_list_name: CustomListName,
    ) -> List[str]:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(
        self, custom_list_name: CustomListName, custom_list_entry_name: str
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)
