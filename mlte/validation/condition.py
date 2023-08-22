"""
mlte/validation/condition.py

The interface for measurement validation.
"""

from __future__ import annotations

import base64
import typing
from typing import Any, Callable, Dict, List

import dill

from mlte.validation.result import Result
from mlte.value.artifact import Value
from mlte.validation.result import Result
from mlte.spec.model import ConditionModel


class Condition:
    """
    The Condition class defines the interface for measurement validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        name: str,
        arguments: List[Any],
        callback: Callable[[Value], Result],
    ):
        """
        Initialize a Condition instance.

        :param name: The name of the name method, for documenting purposes.
        :type name: str
        :param callback: The callable that implements validation
        :type callback: Callable[[Value], Result]
        """

        self.name: str = name
        """The human-readable identifier for the name method."""

        self.arguments: List[Any] = arguments
        """The arguments used when validating the condition."""

        self.callback: Callable[[Value], Result] = callback
        """The callback that implements validation."""

    def __call__(self, value: Value) -> Result:
        """
        Invoke the validation callback

        :param value: The value of measurement evaluation
        :type value: Value

        :return: The result of measurement validation
        :rtype: Result
        """
        return self.callback(value)._with_evidence_metadata(value.metadata)

    def to_model(self) -> ConditionModel:
        """
        Returns this requirement as a model.

        :return: The serialized model object.
        :rtype: ConditionModel
        """
        return ConditionModel(
            name=self.name,
            arguments=self.arguments,
            callback=base64.b64encode(dill.dumps(self.callback)).decode(
                "utf-8"
            ),
        )

    @classmethod
    def from_model(cls, model: ConditionModel) -> Condition:
        """
        Deserialize a Condition from a model.

        :param model: The model.
        :type model: ConditionModel

        :return: The deserialized Condition
        :rtype: Condition
        """
        condition: Condition = Condition(
            model.name,
            model.arguments,
            dill.loads(base64.b64decode(str(model.callback).encode("utf-8"))),
        )
        return condition

    def __str__(self) -> str:
        """Return a string representation of Condition."""
        return f"{self.name}"

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Condition instances for equality."""
        # TODO: is just names enough? Should we compare args and callback?
        if not isinstance(other, Condition):
            return False
        reference: Condition = other
        return self.name == reference.name

    def __neq__(self, other: Condition) -> bool:
        """Compare Condition instances for inequality."""
        return not self.__eq__(other)
