"""DB utils for getting custom list data from the DB."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.custom_list.underlying.rdbs.metadata import DBCustomListEntry


class DBReader:
    """Class encapsulating functions to read custom list related data from the DB."""

    @staticmethod
    def get_entry(
        name: str, session: Session
    ) -> tuple[CustomListEntryModel, DBCustomListEntry]:
        """Reads the custom list entry with the given name using the provided session and returns a CustomListEntryModel and DBCustomListEntry."""
        entry_orm = session.scalar(
            select(DBCustomListEntry).where(DBCustomListEntry.name == name)
        )

        if entry_orm is None:
            raise errors.ErrorNotFound(
                f"Custom List Entry with name {name} was not found in custom list store."
            )
        else:
            return (
                DBReader.create_custom_list_entry_model(entry_orm),
                entry_orm,
            )

    @staticmethod
    def get_list(
        list_name: str, session: Session
    ) -> tuple[list[CustomListEntryModel], list[DBCustomListEntry]]:
        """Reads all entries in specified list in the DB and returns list of CustomListEntryModel and DBCustomLIstEntry objects."""
        list_orm = list(
            session.scalars(
                select(DBCustomListEntry).where(
                    DBCustomListEntry.list_name == list_name
                )
            )
        )
        entries: list[CustomListEntryModel] = []
        for entry_orm in list_orm:
            entry = DBReader.create_custom_list_entry_model(entry_orm)
            entries.append(entry)

        return entries, list_orm

    @staticmethod
    def create_custom_list_entry_orm(
        entry: CustomListEntryModel,
        list_name: CustomListName,
        session: Session,
        entry_orm: Optional[DBCustomListEntry] = None,
    ) -> DBCustomListEntry:
        """Creates or updates the DB object from the corresponding internal model."""
        if entry_orm is None:
            entry_orm = DBCustomListEntry()
        if entry.parent:
            _, entry_orm.parent = DBReader.get_entry(entry.parent, session)

        entry_orm.list_name = list_name
        entry_orm.name = entry.name
        entry_orm.description = entry.description

        return entry_orm

    @staticmethod
    def create_custom_list_entry_model(
        entry_orm: DBCustomListEntry,
    ) -> CustomListEntryModel:
        """Creates the internal model object from the corresponding DB object."""
        return CustomListEntryModel(
            name=entry_orm.name,
            description=entry_orm.description,
            parent=entry_orm.parent.name if entry_orm.parent else None,
        )
