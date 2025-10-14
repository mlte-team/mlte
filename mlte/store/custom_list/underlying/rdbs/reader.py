"""DB utils for getting custom list data from the DB."""

from typing import List, Tuple

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
    def get_entry(
        name: str, session: Session
    ) -> Tuple[CustomListEntryModel, DBCustomListEntry]:
        """Reads the custom list entry with the given name using the provided session, and returns a CustomListEntryModel and DBCustomListEntry."""
        entry_orm = session.scalar(
            select(DBCustomListEntry).where(DBCustomListEntry.name == name)
        )

        if entry_orm is None:
            raise errors.ErrorNotFound(
                f"Custom List Entry with name {name} was not found in custom list store."
            )
        else:
            return (
                create_custom_list_entry_model(entry_orm),
                entry_orm,
            )

    @staticmethod
    def get_list(
        list_name: str, session: Session
    ) -> Tuple[List[CustomListEntryModel], List[DBCustomListEntry]]:
        """Reads all entries in specified list in the DB, returns list of CustomListEntryModel and DBCustomLIstEntry objects."""
        list_orm = list(
            session.scalars(
                select(DBCustomListEntry).where(
                    DBCustomListEntry.list_name == list_name
                )
            )
        )
        entries: List[CustomListEntryModel] = []
        for entry_orm in list_orm:
            entry = create_custom_list_entry_model(entry_orm)
            entries.append(entry)

        return entries, list_orm
