"""
The interface for measurement validation.
"""
from __future__ import annotations

import typing
from typing import Callable, Any
import base64

import dill

from mlte.value import Value
from . import Result


class Condition:
    """
    The Condition class defines the interface for measurement validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        name: str,
        arguments: list[Any],
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

        self.arguments: list[Any] = arguments
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

    def to_json(self) -> dict[str, Any]:
        """
        Returns this requirement as a JSON dictionary.

        :return: The serialized JSON object.
        :rtype: dict[str, Any]        
        """
        return {
            "name": self.name,
            "arguments": self.arguments,
            "callback": base64.b64encode(dill.dumps(self.callback)).decode(
                "utf-8"
            ),
        }

    @staticmethod
    def from_json(document: dict[str, Any]) -> Condition:
        """
        Deserialize a Condition from a JSON-like dict document.

        :param json: The json document
        :type json: dict[str, Any]

        :return: The deserialized Condition
        :rtype: Condition
        """
        if (
            "name" not in document
            or "arguments" not in document
            or "callback" not in document
        ):
            raise RuntimeError("Saved Condition is malformed.")

        condition: Condition = Condition(
            document["name"],
            document["arguments"],
            dill.loads(
                base64.b64decode(str(document["callback"]).encode("utf-8"))
            ),
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
        if not isinstance(other, Condition):
            return False
        reference: Condition = other
        return self.name == reference.name

    def __neq__(self, other: Condition) -> bool:
        """Compare Condition instances for inequality."""
        return not self.__eq__(other)
