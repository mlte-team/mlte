"""
mlte/custom_list/model.py

Model implementation for a custom list.
"""
from __future__ import annotations

from typing import List

from mlte.model import BaseModel

class CustomListModel(BaseModel):
    """A model class representing a custom list."""

    name: str
    """An name to uniquely identify the list."""

    entries: List[CustomListEntryModel] = []
    """A list of entries in the list."""


class CustomListEntryModel(BaseModel):
    """A model class representing a custom list entry."""

    name: str
    """A name to uniquely identify the entry."""

    description: str
    """A description of the the entry."""
