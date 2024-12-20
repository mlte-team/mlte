"""
mlte/custom_list/model.py

Model implementation for a custom list.
"""
from __future__ import annotations

from typing import List

from mlte.model import BaseModel

class CustomList(BaseModel):
    """A model class representing a custom list."""

    name: str
    """An name to uniquely identify the list."""

    entries: List[CustomListEntry] = []
    """A list of entries in the list."""


class CustomListEntry(BaseModel):
    """A model class representing a custom list entry."""

    namme: str
    """A name to uniquely identify the entry."""

    description: str
    """A description of the the entry."""
