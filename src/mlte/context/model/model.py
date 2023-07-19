"""
mlte/context/model/model.py

Model implementation for MLTE context information.
"""

from mlte.model import BaseModel


class NamespaceModel(BaseModel):
    """Model implementation for MLTE namespace."""

    identifier: str
    """The name of the namespace."""


class ModelIdentifierModel(BaseModel):
    """Model implementation for MLTE model identifier."""

    identifier: str
    """The identifier for the model."""


class ModelVersionModel(BaseModel):
    """Model implementation for MLTE model version."""

    identifier: str
    """The identifier for the model version."""
