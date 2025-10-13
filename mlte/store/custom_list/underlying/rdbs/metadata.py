"""Definition of the metadata (DB schema) for the custom list store."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from mlte.custom_list.custom_list_names import CustomListName


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


class DBCustomListEntry(DBBase):
    __tablename__ = "custom_list_entry"

    list_name: Mapped[CustomListName]
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]

    parent: Mapped[str] = mapped_column(
        ForeignKey("custom_list_entry.name"), nullable=True
    )

    def __repr__(self) -> str:
        return f"CustomListEntry(name={self.name!r}, description={self.description!r}, parent={self.parent!r})"
