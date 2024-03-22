"""
mlte/store/user/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the user store.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


# -------------------------------------------------------------------------
# Structural Elements
# -------------------------------------------------------------------------


class DBUser(DBBase):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[Optional[str]]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (UniqueConstraint("username", name="_username"),)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, disabled={self.disabled!r})"
