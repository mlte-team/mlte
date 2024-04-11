"""
mlte/backend/api/model.py

Model implementations for artifact store.

NOTE(Kyle): I am unsure as to how I want to refactor the API to account
for additional meta-models like these. This worked well for write request;
should the other endpoints be refactored to look more like this one?
"""

from pydantic import BaseModel

from mlte.artifact.model import ArtifactModel


class WriteArtifactRequest(BaseModel):
    """Defines the data in a POST request to write an artifact."""

    artifact: ArtifactModel
    """The model for the artifact to write."""

    force: bool = False
    """Indicates that existing artifacts may be overwritten."""

    parents: bool = False
    """Indicates whether organizational elements should be created."""


class WriteArtifactResponse(BaseModel):
    """Defines the data in a response to writing an artifact."""

    artifact: ArtifactModel
    """The model for the artifact that was written."""
