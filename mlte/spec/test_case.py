"""
TestCase defines structure for all tests to be defined for a TestSpec.
"""

from typing import Optional

from mlte.measurement.measurement import Measurement
from mlte.validation.result import Result
from mlte.validation.validator import Validator
from mlte.value.artifact import Value


class TestCase:
    """
    Class that contains all information about a test case.
    """

    def __ini__(
        self,
        name: str,
        goal: str,
        qas_list: list[str],
        measurement: Optional[Measurement] = None,
        validator: Optional[Validator] = None,
    ):
        self.name = name
        """Name or id given to the test case."""

        self.goal = goal
        """Goal for the TestCase, reason for it."""

        self.qas_list = qas_list.copy()
        """Quality Attribute Scenarios that are associated to this test case."""

        self.measurement = measurement
        """Used to measure and get a value for this test case."""

        self.validator = validator
        """Used to validate this test case."""

    def measure(self, *args, **kwargs) -> Value:
        """Executes the configured measurement with the given params."""
        if self.measurement is None:
            raise RuntimeError(
                "Can't evaluate measurement, no measurement has been configured."
            )

        return self.measurement.evaluate(*args, **kwargs)

    def validate(self, value: Value) -> Result:
        """Executes the configured validator with the given Value."""
        if self.validator is None:
            raise RuntimeError(
                "Can't validate, no validator has been configured."
            )

        return self.validator.validate(value)
