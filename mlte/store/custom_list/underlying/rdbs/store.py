"""Implementation of relation database system custom list store."""

from __future__ import annotations

import typing
from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Session

import mlte.store.error as errors
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.base import StoreURI
from mlte.store.common.rdbs_storage import RDBStorage
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import (
    CustomListEntryMapper,
    CustomListStoreSession,
)
from mlte.store.custom_list.underlying.rdbs.factory import (
    create_custom_list_entry_orm,
)
from mlte.store.custom_list.underlying.rdbs.metadata import DBBase
from mlte.store.custom_list.underlying.rdbs.reader import DBReader

# -----------------------------------------------------------------------------
# RDBCustomListStore
# -----------------------------------------------------------------------------


class RDBCustomListStore(CustomListStore):
    """A DB implementation of the MLTE custom list store."""

    def __init__(self, uri: StoreURI, **kwargs) -> None:
        self.storage = RDBStorage(
            uri,
            base_class=typing.cast(DeclarativeBase, DBBase),
            **kwargs,
        )
        """The relational DB storage."""

    def session(self) -> RDBCustomListStoreSession:
        """
        Return a session handle fo the store session.
        :return: The session handle
        """
        return RDBCustomListStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# RDBCustomListStoreSession
# -----------------------------------------------------------------------------


class RDBCustomListStoreSession(CustomListStoreSession):
    """A relational DB implementation of the MLTE custom list store session."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """"RDB storage."""

        self.custom_list_entry_mapper = RDBCustomListEntryMapper(storage)
        """The mapper to entry CRUD"""

    def close(self) -> None:
        """Close the session."""
        self.storage.close()


# -----------------------------------------------------------------------------
# RDBCustomListEntryMapper
# -----------------------------------------------------------------------------


class RDBCustomListEntryMapper(CustomListEntryMapper):
    """RDB mapper mapper for the custom list entry resource."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(
        self,
        new_entry: CustomListEntryModel,
        list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")

        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_entry(new_entry.name, session)
                raise errors.ErrorAlreadyExists(
                    f"Custom list entry with name {new_entry.name} already exists."
                )
            except errors.ErrorNotFound:
                # If entry was not found, it means we can create it.
                entry_orm = create_custom_list_entry_orm(new_entry, list_name)
                session.add(entry_orm)
                session.commit()
                return new_entry

    def read(
        self, entry_name: str, list_name: Optional[CustomListName] = None
    ) -> CustomListEntryModel:
        with Session(self.storage.engine) as session:
            entry, _ = DBReader.get_entry(entry_name, session)
            return entry

    def list(self, list_name: Optional[CustomListName] = None) -> List[str]:
        if list_name is None:
            raise RuntimeError("Custom list name can't be None")
        with Session(self.storage.engine) as session:
            entries, _ = DBReader.get_list(list_name, session)
            return [entry.name for entry in entries]

    def edit(
        self,
        updated_entry: CustomListEntryModel,
        list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        with Session(self.storage.engine) as session:
            _, entry_orm = DBReader.get_entry(updated_entry.name, session)

            # Update existing entry
            entry_orm = create_custom_list_entry_orm(
                updated_entry, entry_orm.list_name, entry_orm
            )
            session.commit()

            stored_entry, _ = DBReader.get_entry(updated_entry.name, session)
            return stored_entry

    def delete(
        self, entry_name: str, list_name: Optional[CustomListName] = None
    ) -> CustomListEntryModel:
        with Session(self.storage.engine) as session:
            entry, entry_orm = DBReader.get_entry(entry_name, session)
            session.delete(entry_orm)
            session.commit()
            return entry
