"""
mlte/evidence/metadata.py

EvidenceMetadata class definition.
"""

from __future__ import annotations

from typing import Optional

from mlte.evidence.identifier import Identifier
from mlte.model.base_model import BaseModel


class EvidenceMetadata(BaseModel):
    """A simple wrapper for evidence metadata."""

    measurement_type: str
    """The name of the measurement class type."""

    identifier: Identifier
    """The identifier for the evidence."""

    info: Optional[str] = None
    """Additional unstructured information to be stored with the metadata."""

    def get_id(self) -> str:
        """Returns the id as a string."""
        return str(self.identifier)

    def __str__(self) -> str:
        """Return a string representation of a EvidenceMetadata."""
        representation = f"{self.measurement_type}-{self.identifier}"
        if self.info is not None:
            representation += f"-{self.info}"
        return representation

    def __eq__(self, other: object) -> bool:
        """Compare instances for equality."""
        if not isinstance(other, EvidenceMetadata):
            return False
        return (
            self.measurement_type == other.measurement_type
            and self.identifier == other.identifier
            and self.info == other.info
        )
