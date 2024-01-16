"""
mlte/catalog/entry/model.py

Model implementation for MLTE catalog entries.
"""

from typing import Optional

from mlte.model import BaseModel


class CatalogEntryHeader(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the entry."""

    author: str
    """The author for the entry."""

    created: Optional[int] = -1
    """The timestamp of creation of this entry, as Unix time."""

    updated: Optional[int] = -1
    """The timestamp of last update of this entry, as Unix time."""


class CatalogEntryModel(BaseModel):
    """The base model for MLTE catalog entries."""

    header: CatalogEntryHeader
    """The header."""

    problem_type: str
    """Tags for the problem type for the entry."""

    problem_domain: str
    """Tags for the problem type for the entry."""

    property_category: str
    """The property category or QA for the entry."""

    property: str
    """The property for the entry."""

    code_type: str
    """The code type the entry."""
    # TODO: change to type, Validaor or Measurement method

    code: str
    """The actual code for the entry."""

    description: str
    """The description of the code for the entry."""

    inputs: str
    """The input for the entry."""

    output: str
    """The output for the entry."""
