"""Model implementation for MLTE catalog entries."""

from typing import Any, Optional

from mlte.model import BaseModel
from mlte.store.query import Filterable


class CatalogEntryHeader(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the entry."""

    creator: Optional[str] = None
    """The username of the author for the entry."""

    created: Optional[int] = -1
    """The timestamp of creation of this entry, as Unix time."""

    updater: Optional[str] = None
    """The username of the author of the last edition."""

    updated: Optional[int] = -1
    """The timestamp of last update of this entry, as Unix time."""

    catalog_id: Optional[str] = None
    """The id of the catalog this entry came from."""


class CatalogEntry(Filterable):
    """The base model for MLTE catalog entries."""

    header: CatalogEntryHeader
    """The header."""

    tags: list[str] = []
    """Tags for the problem for the entry."""

    qa_category: Optional[str] = None
    """The QA category for the entry."""

    quality_attribute: Optional[str] = None
    """The quality attribute for the entry."""

    code: str
    """The actual code for the entry."""

    description: Optional[str] = None
    """The description of the code for the entry."""

    inputs: Optional[str] = None
    """The input for the entry."""

    output: Optional[str] = None
    """The output for the entry."""

    def get_identifier(self) -> str:
        return self.header.identifier

    def get_type(self) -> Any:
        """Just to implement abstract class, not really needed."""
        return "entry"
