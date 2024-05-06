"""
mlte/context/model.py

Model implementation for MLTE context information.
"""

from typing import List

from mlte.model import BaseModel


class VersionCreate(BaseModel):
    """The model that defines the data necessary to create a MLTE version."""

    identifier: str
    """The identifier for the version."""


class Version(BaseModel):
    """Model implementation for MLTE model version."""

    identifier: str
    """The identifier for the model version."""

    # TODO(Kyle): In the future, we may implement new endpoints
    # that allow one to GET /version to get all artifacts associated
    # with a (model, version) duple


class ModelCreate(BaseModel):
    """The model that defines the data necessary to create a MLTE model."""

    identifier: str
    """The identifier for the model."""


class Model(BaseModel):
    """Model implementation for MLTE model identifier."""

    identifier: str
    """The identifier for the model."""

    versions: List[Version]
    """A collection of the model versions."""
