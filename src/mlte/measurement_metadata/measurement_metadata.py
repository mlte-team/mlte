"""
MeasurementMetadata class definition.
"""
from __future__ import annotations

from typing import Any

from .identifier import Identifier


class MeasurementMetadata:
    """A simple wrapper for measurement metadata."""

    def __init__(self, typename: str, identifier: str):
        self.typename = typename
        """The name of the measurement class type."""

        self.identifier = Identifier(identifier)
        """The identifier for the measurement."""

    def to_json(self) -> dict[str, Any]:
        """Serialize to JSON document."""
        return {
            "identifier": self.identifier.to_json(),
            "typename": self.typename,
        }

    @staticmethod
    def from_json(json: dict[str, Any]) -> MeasurementMetadata:
        """Deserialize from JSON document."""
        if "identifier" not in json:
            raise RuntimeError(
                "Cannot deserialize MeasurementMetadata, missing key 'identifier'."
            )
        if "typename" not in json:
            raise RuntimeError(
                "Cannot deserialize MeasurementMetadata, missing key 'typename'."
            )
        return MeasurementMetadata(
            typename=json["typename"], identifier=json["identifier"]["name"]
        )

    def __str__(self) -> str:
        """Return a string representation of a MeasurementMetadata."""
        return f"{self.typename}-{self.identifier}"

    def __eq__(self, other: object) -> bool:
        """Compare instances for equality."""
        if not isinstance(other, MeasurementMetadata):
            return False
        reference: MeasurementMetadata = other
        return (
            self.typename == reference.typename
            and self.identifier == reference.identifier
        )
