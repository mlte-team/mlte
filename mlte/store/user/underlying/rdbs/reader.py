"""
mlte/store/user/underlying/rdbs/reader.py

DB utils for getting user related data from the DB.
"""
from __future__ import annotations

from typing import Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.store.user.underlying.rdbs.metadata import DBUser
from mlte.user.model import User


class DBReader:
    """Class encapsulating functions to read user related data from the DB."""

    @staticmethod
    def get_user(username: str, session: Session) -> Tuple[User, DBUser]:
        """Reads the user with the given user using the provided session, and returns a User and DBUser object."""
        user_obj = session.scalar(
            select(DBUser).where(DBUser.username == username)
        )

        if user_obj is None:
            raise errors.ErrorNotFound(
                f"User with username {username} was not found in the user store."
            )
        else:
            return (
                User(
                    username=user_obj.username,
                    email=user_obj.email,
                    disabled=user_obj.disabled,
                    hashed_password=user_obj.hashed_password,
                ),
                user_obj,
            )
