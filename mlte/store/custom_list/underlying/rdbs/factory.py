"""Conversions betwewen schema and internal models."""

from mlte.custom_list.model import CustomListEntryModel
from mlte.store.custom_list.underlying.rdbs.metadata import DBCustomListEntry


def create_custom_list_entry_orm(
    entry: CustomListEntryModel,
) -> DBCustomListEntry:
    """Creats the DB object from the corresponding internal model."""
    entry_orm = DBCustomListEntry(
        name=entry.name,
        description=entry.description,
        parent=entry.parent,
    )
    return entry_orm

def create_custom_list_entry_model(entry_orm: DBCustomListEntry) -> CustomListEntryModel:
    """Creats the internal model object from the corresponding DB object."""
    entry = CustomListEntryModel(
        name=entry_orm.name,
        description=entry_orm.description,
        parent=entry_orm.parent,
    )
    return entry