"""
mlte/catalog/entry/model.py

Model implementation for MLTE catalog entries.
"""

from typing import List, Optional

from strenum import StrEnum

from mlte.model import BaseModel


class CatalogEntryType(StrEnum):
    """Types of catalog entries."""

    MEASUREMENT = "measurement"
    """Classes that calculate a metric."""

    VALIDATION = "validation"
    """Validator method or class that compare measuremets to conditions."""


class CatalogEntryHeader(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the entry."""

    creator: Optional[str] = None
    """The author for the entry."""

    created: Optional[int] = -1
    """The timestamp of creation of this entry, as Unix time."""

    updated: Optional[int] = -1
    """The timestamp of last update of this entry, as Unix time."""


class CatalogEntry(BaseModel):
    """The base model for MLTE catalog entries."""

    header: CatalogEntryHeader
    """The header."""

    problem_type: List[str] = []
    """Tags for the problem type for the entry."""

    problem_domain: List[str] = []
    """Tags for the problem type for the entry."""

    property_category: Optional[str] = None
    """The property category or QA for the entry."""

    property: Optional[str] = None
    """The property for the entry."""

    code_type: CatalogEntryType
    """The code type the entry."""

    code: str
    """The actual code for the entry."""

    description: Optional[str] = None
    """The description of the code for the entry."""

    inputs: Optional[str] = None
    """The input for the entry."""

    output: Optional[str] = None
    """The output for the entry."""
