"""
mlte/store/models/data_model.py

Data model implementation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ValueVersion(BaseModel):
    """Represents an individual value version."""

    # The version identifier
    version: int
    # The value payload
    data: Dict[str, Any]

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        return {"version": self.version, "data": self.data}

    @staticmethod
    def from_json(json: Dict[str, Any]):
        """Deserialize from JSON object."""
        assert all(
            n in json for n in ["version", "data"]
        ), "Broken precondition."
        return ValueVersion(version=json["version"], data=json["data"])


class Value(BaseModel):
    """Represents an individual value (a collection of versions)."""

    # The identifier for the value
    identifier: str
    # The tag associated with the value
    tag: Optional[str] = None
    # A collection of value versions
    versions: List[ValueVersion]

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        return {
            "identifier": self.identifier,
            "tag": self.tag if self.tag is not None else "",
            "versions": [v.to_json() for v in self.versions],
        }

    @staticmethod
    def from_json(json: Dict[str, Any]):
        """Deserialize from JSON object."""
        assert all(
            n in json for n in ["identifier", "tag", "versions"]
        ), "Broken precondition."
        return Value(
            identifier=json["identifier"],
            tag=None if json["tag"] == "" else json["tag"],
            versions=[ValueVersion.from_json(v) for v in json["versions"]],
        )


class ModelIdentifier:
    """Represents a model identifier string."""

    def __init__(self, identifier: str):
        self.identifier = identifier

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        return {"identifier": self.identifier}


class ModelVersion:
    """Represents a model version string."""

    def __init__(self, version: str):
        self.version = version

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        return {"version": self.version}


class ModelMetadata:
    """Represents the metadata returned for a model."""

    def __init__(
        self, identifier: ModelIdentifier, versions: List[ModelVersion]
    ):
        self.identifier = identifier
        self.versions = versions

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        # TODO(Kyle): Sort by creation timestamp?
        return {
            "identifier": self.identifier.to_json(),
            "versions": [v.to_json() for v in self.versions],
        }
