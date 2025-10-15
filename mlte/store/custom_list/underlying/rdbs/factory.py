"""Conversions betwewen schema and internal models."""

from typing import Optional

from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.custom_list.underlying.rdbs.metadata import DBCustomListEntry


def create_custom_list_entry_orm(
    entry: CustomListEntryModel,
    list_name: CustomListName,
    entry_orm: Optional[DBCustomListEntry] = None,
    parent_id: Optional[int] = None,
) -> DBCustomListEntry:
    """Creates or updates the DB object from the corresponding internal model."""
    if entry_orm is None:
        entry_orm = DBCustomListEntry()

    entry_orm.list_name = list_name
    entry_orm.name = entry.name
    entry_orm.description = entry.description
    entry_orm.parent = parent_id

    return entry_orm


def create_custom_list_entry_model(
    entry_orm: DBCustomListEntry,
    parent_name: Optional[str] = None,
) -> CustomListEntryModel:
    """Creates the internal model object from the corresponding DB object."""
    return CustomListEntryModel(
        name=entry_orm.name,
        description=entry_orm.description,
        parent=parent_name,
    )
