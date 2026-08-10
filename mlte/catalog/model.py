"""Model implementation for MLTE catalog entries."""

from mlte.model import BaseModel
from mlte.store.query import Filterable


class CatalogEntryHeader(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the entry."""

    creator: str | None = None
    """The username of the author for the entry."""

    created: int | None = -1
    """The timestamp of creation of this entry, as Unix time."""

    updater: str | None = None
    """The username of the author of the last edition."""

    updated: int | None = -1
    """The timestamp of last update of this entry, as Unix time."""

    catalog_id: str | None = None
    """The id of the catalog this entry came from."""


class CatalogEntry(Filterable):
    """The base model for MLTE catalog entries."""

    header: CatalogEntryHeader
    """The header."""

    tags: list[str] = []
    """Tags for the problem for the entry."""

    quality_attribute: str = ""
    """The quality attribute for the entry."""

    code: str
    """The actual code for the entry."""

    description: str | None = None
    """The description of the code for the entry."""

    inputs: str | None = None
    """The input for the entry."""

    output: str | None = None
    """The output for the entry."""

    def get_identifier(self) -> str:
        return self.header.identifier
