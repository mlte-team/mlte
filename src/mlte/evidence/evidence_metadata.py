"""
EvidenceMetadata class definition.
"""
from __future__ import annotations

from typing import Any, Optional

from .identifier import Identifier


class EvidenceMetadata:
    """A simple wrapper for evidence metadata."""

    def __init__(
        self, measurement_type: str, identifier: str, info: Optional[str] = None
    ):
        self.measurement_type = measurement_type
        """The name of the measurement class type."""

        self.identifier = Identifier(identifier)
        """The identifier for the measurement."""

        self.additional_info: Optional[str] = info
        """Additional unstructured information to be stored with the metadata."""

    def get_id(self) -> str:
        """Returns the id as a string."""
        return str(self.identifier)

    def to_json(self) -> dict[str, Any]:
        """Serialize to JSON document."""
        doc = {
            "identifier": self.identifier.to_json(),
            "measurement_type": self.measurement_type,
        }
        if self.additional_info is not None:
            doc["additional_info"] = self.additional_info
        return doc

    @staticmethod
    def from_json(json: dict[str, Any]) -> EvidenceMetadata:
        """Deserialize from JSON document."""
        if "identifier" not in json:
            raise RuntimeError(
                "Cannot deserialize EvidenceMetadata, missing key 'identifier'."
            )
        if "measurement_type" not in json:
            raise RuntimeError(
                "Cannot deserialize EvidenceMetadata, missing key 'measurement_type'."
            )

        additional_info: Optional[str] = (
            json["additional_info"] if "additional_info" in json else None
        )

        metadata = EvidenceMetadata(
            measurement_type=json["measurement_type"],
            identifier=json["identifier"],
            info=additional_info,
        )
        return metadata

    def __str__(self) -> str:
        """Return a string representation of a EvidenceMetadata."""
        representation = f"{self.measurement_type}-{self.identifier}"
        if self.additional_info is not None:
            representation += f"-{self.additional_info}"
        return representation

    def __eq__(self, other: object) -> bool:
        """Compare instances for equality."""
        if not isinstance(other, EvidenceMetadata):
            return False
        reference: EvidenceMetadata = other
        return (
            self.measurement_type == reference.measurement_type
            and self.identifier == reference.identifier
            and self.additional_info == reference.additional_info
        )
