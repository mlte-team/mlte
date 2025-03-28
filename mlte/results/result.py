"""
mlte/validation/result.py

The result of measurement validation.
"""

from __future__ import annotations

import sys
from abc import ABC
from typing import Optional

import mlte._private.meta as meta
from mlte.evidence.metadata import EvidenceMetadata
from mlte.results.model import ResultModel

# -----------------------------------------------------------------------------
# Validation Results
# -----------------------------------------------------------------------------


class Result(ABC):
    """The base class for measurement validation results."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete Result."""
        return meta.has_callables(subclass, "__bool__", "__str__")

    def __init__(self, message: str):
        """Initialize a Result instance."""

        self.message = message
        """The message indicating the reason for status."""

        self.evidence_metadata: Optional[EvidenceMetadata] = None
        """
        The measurement id from which this was obtained.
        """

    def _with_evidence_metadata(
        self, evidence_metadata: Optional[EvidenceMetadata]
    ) -> Result:
        """
        Set the `metadata` field of the Result
        to indicate the evidence metadata info from which
        it was generated.

        This hook allows us to embed the evidence metadata within
        the Result so that we can use the metadata
        information later when it is used to generate a report.

        :param evidence_metadata: The evidence metadata to be added.
        :return: The Result instance (`self`)
        """
        self.evidence_metadata = evidence_metadata
        return self

    def to_model(self) -> ResultModel:
        """
        Returns this object as a model

        :return: The model.
        """
        return ResultModel(
            type=f"{self}",
            message=self.message,
            evidence_metadata=self.evidence_metadata,
        )

    @classmethod
    def from_model(cls, model: ResultModel) -> Result:
        """
        Returns a result from a model.

        :param model: The model
        :return: The deserialized object.
        """
        result_type = model.type
        results_module = sys.modules[__name__]
        result_class = getattr(results_module, result_type)

        result: Result = result_class(model.message)
        result = result._with_evidence_metadata(model.evidence_metadata)
        return result

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        assert self.evidence_metadata is not None, "Broken precondition."
        if not isinstance(other, Result):
            return False
        return self.to_model() == other.to_model()


class Success(Result):
    """Indicates successful measurement validation."""

    def __init__(self, message: str = ""):
        """
        Initialize a Success validation result instance.

        :param message: Optional message
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
        """
        super().__init__(message)

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return False

    def __str__(self) -> str:
        """String representation."""
        return "Failure"


class Info(Result):
    """Indicates an informational resut of measurement validation, not validated."""

    def __init__(self, message: str):
        """
        Initialize an Info validatation result instance.

        :param message: Message indicating the reason validation is info
        """
        super().__init__(message)

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise RuntimeError("Boolean conversion for Info() is ambiguous.")

    def __str__(self) -> str:
        """String representation."""
        return "Info"
