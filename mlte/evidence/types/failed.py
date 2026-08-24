"""
An Evidence instance for a failure in the measurement process.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceType, FailedValueModel
from mlte.model.base_model import BaseModel


class FailedException(Exception):
    """Exception raised when an failed evidence is found processing fails.

    Attributes:
        failed_evidence -- the encapsulated Failed object
    """

    def __init__(self, failed_item: Failed):
        self.failed_evidence = failed_item
        super().__init__(f"Evidence gathering failed: {failed_item.details}")


class Failed(Evidence):
    """
    Failed implements the Value interface for a failed evidence.
    """

    def __init__(self, details: str, traceback: str | None):
        """
        Initialize an instance.
        :param details: The failure details.
        """
        assert isinstance(details, str), "Argument must be `string`."
        super().__init__()

        self.details = details
        """The details."""

        self.traceback = traceback
        """Detailed traceback."""

    def to_model(self) -> ArtifactModel:
        """
        Convert a value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=FailedValueModel(
                details=self.details, traceback=self.traceback
            )
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Failed:
        """
        Convert a value model to its corresponding artifact.
        :param model: The model representation
        :return: The failed value
        """
        body = cls._check_proper_types(model, EvidenceType.FAILED)
        return Failed(
            details=body.value.details,  # type: ignore
            traceback=body.value.traceback,  # type: ignore
        ).with_metadata(body.metadata)

    def __eq__(self, other: object) -> bool:
        """Comparison between values."""
        if not isinstance(other, Failed):
            return False
        return self._equal(other)

    def __str__(self) -> str:
        """Return a string representation of this Evidence."""
        return f"{self.details}"

    # Overriden.
    @classmethod
    def load(cls, identifier: str | None = None) -> Failed:
        evidence = super().load(identifier)
        return typing.cast(Failed, evidence)
