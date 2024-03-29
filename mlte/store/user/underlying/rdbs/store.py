"""
mlte/store/user/underlying/rdbs/store.py

Implementation of relational database system user store.
"""
from __future__ import annotations

from typing import List

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.store.base import StoreURI
from mlte.store.user.store import UserStore, UserStoreSession
from mlte.store.user.underlying.rdbs.metadata import DBBase, DBUser
from mlte.store.user.underlying.rdbs.reader import DBReader
from mlte.user.model import User, UserCreate
from mlte.user.model_logic import convert_user_create_to_user

# -----------------------------------------------------------------------------
# RelationalDBUserStore
# -----------------------------------------------------------------------------


class RelationalDBUserStore(UserStore):
    """A DB implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI, **kwargs) -> None:
        super().__init__(uri=uri)

        self.engine = sqlalchemy.create_engine(uri.uri, **kwargs)
        """The underlying storage for the store."""

        # Create the DB if it doesn't exist already.
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

        # Creates the DB items if they don't exist already.
        self._create_tables()
        self._init_default_user()

    def session(self) -> RelationalDBUserStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBUserStoreSession(engine=self.engine)

    def _create_tables(self):
        """Creates all items, if they don't exist already."""
        DBBase.metadata.create_all(self.engine)


# -----------------------------------------------------------------------------
# RelationalDBUserStoreSession
# -----------------------------------------------------------------------------


class RelationalDBUserStoreSession(UserStoreSession):
    """A relational DB implementation of the MLTE user store session."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        self.engine.dispose()

    # -------------------------------------------------------------------------
    # User CRUD Elements
    # -------------------------------------------------------------------------

    def create_user(self, user: UserCreate) -> User:
        with Session(self.engine) as session:
            try:
                _, _ = DBReader.get_user(user.username, session)
                raise errors.ErrorAlreadyExists(
                    f"User with identifier {user.username} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                # Hash password and create a user with hashed passwords to be stored.
                hashed_user = convert_user_create_to_user(user)
                user_obj = DBUser(
                    username=hashed_user.username,
                    email=hashed_user.email,
                    full_name=hashed_user.full_name,
                    disabled=hashed_user.disabled,
                    hashed_password=hashed_user.hashed_password,
                )
                session.add(user_obj)
                session.commit()
                return hashed_user

    def edit_user(self, user: UserCreate) -> User:
        with Session(self.engine) as session:
            hashed_user = convert_user_create_to_user(user)
            _, user_obj = DBReader.get_user(hashed_user.username, session)

            # Update existing user.
            user_obj.username = hashed_user.username
            user_obj.email = hashed_user.email
            user_obj.full_name = hashed_user.full_name
            user_obj.disabled = hashed_user.disabled
            user_obj.hashed_password = hashed_user.hashed_password
            session.commit()

            return hashed_user

    def read_user(self, username: str) -> User:
        with Session(self.engine) as session:
            user, _ = DBReader.get_user(username, session)
            return user

    def list_users(self) -> List[str]:
        users: List[str] = []
        with Session(self.engine) as session:
            user_objs = session.scalars(select(DBUser))
            for user_obj in user_objs:
                users.append(user_obj.username)
        return users

    def delete_user(self, username: str) -> User:
        with Session(self.engine) as session:
            user, user_obj = DBReader.get_user(username, session)
            session.delete(user_obj)
            session.commit()
            return user
