"""
mlte/store/user/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the user store.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import UniqueConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from mlte.store.user.underlying.default_user import (
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
)


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


class DBUser(DBBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[Optional[str]]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (UniqueConstraint("username", name="_username"),)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, disabled={self.disabled!r})"


def init_default_user(session: Session):
    """Initializes the table with the configured classification types."""
    if session.scalars(select(DBUser)).first() is None:
        user = DBUser(
            username=DEFAULT_USERNAME,
            hashed_password=DEFAULT_PASSWORD,
        )
        session.add(user)
        session.commit()
