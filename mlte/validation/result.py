"""
mlte/validation/result.py

The result of measurement validation.
"""

from __future__ import annotations

import abc
import sys
from typing import Optional

import mlte._private.meta as meta
from mlte.evidence.metadata import EvidenceMetadata
from mlte.validation.model import ResultModel

# -----------------------------------------------------------------------------
# Validation Results
# -----------------------------------------------------------------------------


class Result(metaclass=abc.ABCMeta):
    """The base class for measurement validation results."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete Result."""
        return meta.has_callables(subclass, "__bool__", "__str__")

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
        :return: The Result instance (`self`)
        """
        self.metadata = evidence_metadata
        return self

    def to_model(self) -> ResultModel:
        """
        Returns this object as a model

        :return: The model.
        """
        return ResultModel(
            type=f"{self}", message=self.message, metadata=self.metadata
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
        if model.metadata is not None:
            result = result._with_evidence_metadata(model.metadata)
        return result

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        assert self.metadata is not None, "Broken precondition."
        if not isinstance(other, Result):
            return False
        return self.to_model() == other.to_model()

    def __neq__(self, other: object) -> bool:
        """Inequality comparison."""
        return not self.__eq__(other)


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


class Ignore(Result):
    """Indicates ignored measurement validation."""

    def __init__(self, message: str):
        """
        Initialize an Ignore validatation result instance.

        :param message: Message indicating the reason validation is ignored
        """
        super().__init__(message)

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise RuntimeError("Boolean conversion for Ignore() is ambiguous.")

    def __str__(self) -> str:
        """String representation."""
        return "Ignore"
