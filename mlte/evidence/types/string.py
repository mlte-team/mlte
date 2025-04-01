"""
An Evidence instance for a string value.
"""

from __future__ import annotations

import typing
from typing import Callable

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType, StringValueModel
from mlte.model.base_model import BaseModel
from mlte.validation.validator import Validator


class String(Evidence):
    """
    String implements the Evidence interface for a single real value.
    """

    def __init__(self, value: str):
        """
        Initialize a String instance.
        :param value: The string value
        """
        assert isinstance(value, str), "Argument must be `string`."

        super().__init__()

        self.value = value
        """The attribute to store the string in."""

    def to_model(self) -> ArtifactModel:
        """
        Convert a string value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=StringValueModel(string=self.value)
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> String:
        """
        Convert a string value model to its corresponding artifact.
        :param model: The model representation
        :return: The string value
        """
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.evidence_type == EvidenceType.STRING
        ), "Broken Precondition."
        return String(value=body.value.string).with_metadata(body.metadata)

    @classmethod
    def contains(cls, substring: str) -> Validator:
        """Checks if the given string is in this one."""
        bool_exp: Callable[[String], bool] = (
            lambda value: substring in value.value
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Substring '{substring}' is contained in the string value.",
            failure=f"Substring '{substring}' is not contained in the string value.",
            input_types=[String],
        )
        return validator

    @classmethod
    def equal_to(cls, other_string: str) -> Validator:
        """Checks if the given string is the same as this one in value."""
        bool_exp: Callable[[String], bool] = (
            lambda value: other_string == value.value
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"String '{other_string}' is equal to the internal string value.",
            failure=f"String '{other_string}' is not equal to the internal string value.",
            input_types=[String],
        )
        return validator

    def __str__(self) -> str:
        """Return a string representation of the value."""
        return f"{self.value}"

    def __eq__(self, other: object) -> bool:
        """Comparison between String values."""
        if not isinstance(other, String):
            return False
        return self._equal(other)
