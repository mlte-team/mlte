"""
EvidenceMetadata class definition.
"""
from __future__ import annotations

from typing import Any

from .identifier import Identifier


class EvidenceMetadata:
    """A simple wrapper for evidence metadata."""

    def __init__(self, typename: str, identifier: str):
        self.typename = typename
        """The name of the measurement class type."""

        self.identifier = Identifier(identifier)
        """The identifier for the measurement."""

    def get_id(self) -> str:
        """Returns the id as a string."""
        return str(self.identifier)

    def to_json(self) -> dict[str, Any]:
        """Serialize to JSON document."""
        return {
            "identifier": self.identifier.to_json(),
            "typename": self.typename,
        }

    @staticmethod
    def from_json(json: dict[str, Any]) -> EvidenceMetadata:
        """Deserialize from JSON document."""
        if "identifier" not in json:
            raise RuntimeError(
                "Cannot deserialize EvidenceMetadata, missing key 'identifier'."
            )
        if "typename" not in json:
            raise RuntimeError(
                "Cannot deserialize EvidenceMetadata, missing key 'typename'."
            )
        return EvidenceMetadata(
            typename=json["typename"], identifier=json["identifier"]["name"]
        )

    def __str__(self) -> str:
        """Return a string representation of a EvidenceMetadata."""
        return f"{self.typename}-{self.identifier}"

    def __eq__(self, other: object) -> bool:
        """Compare instances for equality."""
        if not isinstance(other, EvidenceMetadata):
            return False
        reference: EvidenceMetadata = other
        return (
            self.typename == reference.typename
            and self.identifier == reference.identifier
        )
