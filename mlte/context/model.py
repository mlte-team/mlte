"""
mlte/context/model.py

Model implementation for MLTE context information.
"""

from typing import List

from mlte.model import BaseModel


class Version(BaseModel):
    """Model implementation for MLTE model version."""

    identifier: str
    """The identifier for the model version."""


class Model(BaseModel):
    """Model implementation for MLTE model identifier."""

    identifier: str
    """The identifier for the model."""

    versions: List[Version] = []
    """A collection of the model versions."""
