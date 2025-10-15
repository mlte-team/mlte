"""DB utils for getting custom list data from the DB."""

from sqlalchemy import select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.custom_list.underlying.rdbs.factory import (
    create_custom_list_entry_model,
)
from mlte.store.custom_list.underlying.rdbs.metadata import DBCustomListEntry


class DBReader:
    """Class encapsulating functions to read custom list related data from the DB."""

    @staticmethod
    def get_entry_by_name(
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
            parent_orm = None
            if entry_orm.parent:
                _, parent_orm = DBReader.get_entry_by_id(
                    entry_orm.parent, session
                )

            return (
                create_custom_list_entry_model(
                    entry_orm, parent_orm.name if parent_orm else None
                ),
                entry_orm,
            )

    @staticmethod
    def get_entry_by_id(
        id: int, session: Session
    ) -> tuple[CustomListEntryModel, DBCustomListEntry]:
        """Reads the custom list entry with the given id using the provided session and returns a CustomListEntryModel and DBCustomListEntry."""
        entry_orm = session.scalar(
            select(DBCustomListEntry).where(DBCustomListEntry.id == id)
        )

        if entry_orm is None:
            raise errors.ErrorNotFound(
                f"Custom List Entry with id {id} was not found in custom list store."
            )
        else:
            parent_orm = None
            if entry_orm.parent:
                _, parent_orm = DBReader.get_entry_by_id(
                    entry_orm.parent, session
                )

            return (
                create_custom_list_entry_model(
                    entry_orm, parent_orm.name if parent_orm else None
                ),
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
            parent_orm = None
            if entry_orm.parent:
                _, parent_orm = DBReader.get_entry_by_id(
                    entry_orm.parent, session
                )

            entry = create_custom_list_entry_model(
                entry_orm, parent_orm.name if parent_orm else None
            )
            entries.append(entry)

        return entries, list_orm
