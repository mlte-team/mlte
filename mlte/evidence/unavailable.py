"""
An Evidence instance for a problem in the measurement process that resulted in unavailable evidence.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceType, UnavailableValueModel
from mlte.model.base_model import BaseModel


class UnavailableException(Exception):
    """Exception raised when an unavailable evidence is found while processing evidence.

    Attributes:
        unavailable -- the encapsulated Unavailable object
    """

    def __init__(self, unavailable: Unavailable):
        self.unavailable = unavailable
        super().__init__(f"Evidence gathering failed: {unavailable.details}")


class Unavailable(Evidence):
    """
    Implements the Evidence interface for evidence that could not be obtained due to a problem.
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
            value_model=UnavailableValueModel(
                details=self.details, traceback=self.traceback
            )
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Unavailable:
        """
        Convert a value model to its corresponding artifact.
        :param model: The model representation
        :return: The failed value
        """
        body = cls._check_proper_types(model, EvidenceType.UNAVAILABLE)
        return Unavailable(
            details=body.value.details,  # type: ignore
            traceback=body.value.traceback,  # type: ignore
        ).with_metadata(body.metadata)

    def __eq__(self, other: object) -> bool:
        """Comparison between values."""
        if not isinstance(other, Unavailable):
            return False
        return self._equal(other)

    def __str__(self) -> str:
        """Return a string representation of this Evidence."""
        return f"{self.details}"

    # Overriden.
    @classmethod
    def load(cls, identifier: str | None = None) -> Unavailable:
        evidence = super().load(identifier)
        return typing.cast(Unavailable, evidence)
