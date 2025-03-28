"""MLTE custom list store interface implementation"""

from __future__ import annotations

from typing import List, Optional, cast

import mlte.store.error as errors
from mlte.custom_list.custom_list_names import (
    CustomListName,
    CustomListParentMappings,
)
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
        custom_list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(
        self,
        updated_custom_list_entry: CustomListEntryModel,
        custom_list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def read(
        self,
        custom_list_entry_name: str,
        custom_list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def list(
        self,
        custom_list_name: Optional[CustomListName] = None,
    ) -> List[str]:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(
        self,
        custom_list_entry_name: str,
        custom_list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def _ensure_parent_exists(
        self, parent: str, list_name: Optional[CustomListName]
    ) -> None:
        if list_name in CustomListParentMappings.parent_mappings.keys():
            if parent not in self.list(
                CustomListName(
                    CustomListParentMappings.parent_mappings[list_name]
                )
            ):
                raise errors.ErrorNotFound(
                    f"Parent {parent} does not exist in list {CustomListParentMappings.parent_mappings[list_name]}"
                )
        elif parent != "":
            raise errors.InternalError(
                "Parent specified for item in list with no parent list."
            )

    def _delete_children(
        self, list_name: Optional[CustomListName], entry_name: str
    ) -> None:
        """Cascades delete to children of a parent."""
        child_list_name = CustomListParentMappings.get_child_list_name(
            list_name
        )
        if child_list_name:
            for child_entry_name in self.list(CustomListName(child_list_name)):
                child_entry = self.read(child_entry_name, child_list_name)
                if child_entry.parent == entry_name:
                    self.delete(child_entry_name, child_list_name)
