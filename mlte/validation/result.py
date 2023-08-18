"""
mlte/validation/result.py

The result of measurement validation.
"""

from __future__ import annotations

import abc
from typing import Optional, Any, Dict
import sys

from mlte.evidence.metadata import EvidenceMetadata


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


# -----------------------------------------------------------------------------
# Validation Results
# -----------------------------------------------------------------------------


class Result(metaclass=abc.ABCMeta):
    """The base class for measurement validation results."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete Result."""
        return all(
            _has_callable(subclass, method)
            for method in ["__bool__", "__str__"]
        )

    def __init__(self, message: str):
        """
        Initialize a Result instance.
        """

        self.message = message
        """The message indicating the reason for status."""

        self.metadata: Optional[EvidenceMetadata] = None
        """
        The information about the measurement from which this was obtained.
        """

    def _with_evidence_metadata(
        self, evidence_metadata: EvidenceMetadata
    ) -> Result:
        """
        Set the `metadata` field of the Result
        to indicate the evidence metadata info from which
        it was generated.

        This hook allows us to embed the evidence metadata within
        the Result so that we can use the metadata
        information later when it is used to generate a report.

        :param evidence_metadata: The evidence metadata of the
        Value from which was this instance was generated.
        :type evidence_metadata: EvidenceMetadata

        :return: The Result instance (`self`)
        :rtype: Result
        """
        self.metadata = evidence_metadata
        return self

    def to_json(self) -> Dict[str, str]:
        """
        Returns this object as a JSON dictionary.

        :return: A JSON-like dictionary with this object.
        :rtype: Dict[str, str]
        """
        doc: Dict[str, Any] = {
            "result_type": f"{self}",
            "message": self.message,
        }
        if self.metadata is not None:
            doc["metadata"] = self.metadata.to_json()
        return doc

    @classmethod
    def from_json(cls, document: Dict[str, Any]) -> Result:
        """
        Returns a result from a serialized JSON string.

        :param json: The json document
        :type json: Dict[str, Any]

        :return: The deserialized object.
        :rtype: Result
        """
        if (
            "result_type" not in document
            or "message" not in document
            or "metadata" not in document
        ):
            raise RuntimeError("Saved Result is malformed.")

        result_type = document["result_type"]
        results_module = sys.modules[__name__]
        result_class = getattr(results_module, result_type)

        result: Result = result_class(document["message"])
        result = result._with_evidence_metadata(
            EvidenceMetadata(**document["metadata"])
        )
        return result

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        assert self.metadata is not None, "Broken precondition."
        if not isinstance(other, Result):
            return False
        return self.metadata.identifier == other.metadata.identifier  # type: ignore

    def __neq__(self, other: object) -> bool:
        """Inequality comparison."""
        return not self.__eq__(other)


class Success(Result):
    """Indicates successful measurement validation."""

    def __init__(self, message: str = ""):
        """
        Initialize a Success validation result instance.

        :param message: Optional message
        :type message: str
        """
        super().__init__(message)

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return True

    def __str__(self) -> str:
        """String representation."""
        return "Success"


class Failure(Result):
    """Indicates failed measurement validation."""

    def __init__(self, message: str = ""):
        """
        Initialize a Failure validation result instance.

        :param message: Optional message
        :type message: str
        """
        super().__init__(message)

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return False

    def __str__(self) -> str:
        """String representation."""
        return "Failure"


class Ignore(Result):
    """Indicates ignored measurement validation."""

    def __init__(self, message: str):
        """
        Initialize an Ignore validatation result instance.

        :param message: Message indicating the reason validation is ignored
        :type message: str
        """
        super().__init__(message)

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise RuntimeError("Boolean conversion for Ignore() is ambiguous.")

    def __str__(self) -> str:
        """String representation."""
        return "Ignore"
