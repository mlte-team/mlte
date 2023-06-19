"""
mlte/value/value.py

Indicates the outcome of measurement evaluation.
"""
from __future__ import annotations

import abc

from typing import Any, Optional

from mlte._global import global_state
from mlte.api import read_value, write_value
from mlte._private.schema import VALUE_LATEST_SCHEMA_VERSION

from mlte.evidence.evidence_metadata import EvidenceMetadata


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Value(metaclass=abc.ABCMeta):
    """
    The Value class serves as the base class of all
    semantically-enriched measurement evaluation values.
    The Value provides a common interface for inspecting
    the results of measurement evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating measurement.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all Value subclasses."""
        # All subclasses of Value must define serialize() and deserialize()
        return all(
            _has_callable(subclass, method)
            for method in ["serialize", "deserialize"]
        )

    def __init__(self, instance, evidence_metadata: EvidenceMetadata):
        """
        Initialize a Value instance.

        :param instance: The subclass instance
        :type instance: Value
        :param evidence_metadata: The generating measurement's metadata
        :type measurement: EvidenceMetadata
        """
        self.metadata = evidence_metadata
        """The info about the generating measurement."""

        self.typename = type(instance).__name__
        """The type of the value itself."""

    @abc.abstractmethod
    def serialize(self) -> dict[str, Any]:
        """TODO"""
        raise NotImplementedError("Cannot serialize abstract Value.")

    @staticmethod
    @abc.abstractmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json: dict[str, Any]
    ) -> Any:
        """TODO"""
        raise NotImplementedError("Cannot deserialize abstract Value.")

    def save(self, tag: Optional[str] = None):
        """
        Save value data to the configured artifact store.

        :param tag: An optional tag to identify groups of results
        :type tag: str
        """
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Use API to save to artifact store
        write_value(
            artifact_store_uri,
            model_identifier,
            model_version,
            self.metadata.identifier.name,
            {
                "schema_version": VALUE_LATEST_SCHEMA_VERSION,
                "metadata": self._serialize_metadata(),
                "payload": {**self.serialize()},
            },
            tag,
        )

    @classmethod
    def load(cls, identifier: str, version: Optional[int] = None) -> Value:
        """
        Load non-semantically-enriched value data from an artifact store.
        This data may then be passed to the type-specific load() method to
        fully-reconstruct the loaded value.

        :param identifier: The identifier for the value
        :type identifier: str
        :param version: The optional version identifier; when not specified,
        the latest version of the value is read
        :type version: int

        :return: The loaded value
        :rtype: Value
        """
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Use API to load from artifact store
        json = read_value(
            artifact_store_uri,
            model_identifier,
            model_version,
            identifier,
            version,
        )

        # TODO: Validate response

        metadata = json["metadata"]
        value: Value = cls.deserialize(
            EvidenceMetadata.from_json(metadata["measurement"]),
            json["payload"],
        )
        return value

    def _serialize_metadata(self) -> dict[str, Any]:
        """Return the header for serialization."""
        return {
            "measurement": self.metadata.to_json(),
            "value": {"typename": self.typename},
        }
