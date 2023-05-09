"""
The interface for measurement validation.
"""

import typing
from typing import Callable
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
        callback: Callable[[Value], Result],
    ):
        """
        Initialize a Condition instance.

        :param name: The condition identifier
        :type name: str
        :param callback: The callable that implements validation
        :type callback: Callable[[Value], Result]
        """
        self.name: str = name
        """The human-readable identifier for the Condition."""

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
        return (
            self.callback(value)
            ._from_condition(self)
            ._with_evidence_metadata(value.metadata)
        )
