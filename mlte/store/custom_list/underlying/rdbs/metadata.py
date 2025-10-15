"""Definition of the metadata (DB schema) for the custom list store."""

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from mlte.custom_list.custom_list_names import CustomListName


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


class DBCustomListEntry(DBBase):
    __tablename__ = "custom_list_entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    list_name: Mapped[CustomListName]
    name: Mapped[str]
    description: Mapped[str]

    parent: Mapped[Optional[int]] = mapped_column(
        ForeignKey("custom_list_entry.id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"CustomListEntry(id={self.id!r}, list_name={self.list_name!r}, name={self.name!r}, description={self.description!r}), parent={self.parent!r}"
