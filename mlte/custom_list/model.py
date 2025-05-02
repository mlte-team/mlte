"""Model implementation for a custom list."""

from __future__ import annotations

from typing import List

from mlte.custom_list.custom_list_names import CustomListName
from mlte.model import BaseModel


class CustomListModel(BaseModel):
    """A model class representing a custom list."""

    name: CustomListName
    """An name to uniquely identify the list."""

    entries: List[CustomListEntryModel] = []
    """A list of entries in the list."""


class CustomListEntryModel(BaseModel):
    """A model class representing a custom list entry."""

    name: str
    """A name to uniquely identify the entry."""

    description: str
    """A description of the the entry."""

    parent: str
    """ID of parent."""

    def __str__(self) -> str:
        if self.parent:
            return f"{self.name} (Parent: {self.parent}): {self.description}"
        else:
            return f"{self.name} (Parent: None): {self.description}"
