"""
TestCase defines structure for all tests to be defined for a TestSpec.
"""

from __future__ import annotations

from typing import Optional

from mlte.measurement.measurement import Measurement
from mlte.spec.model import TestCaseModel
from mlte.validation.result import Result
from mlte.validation.validator import Validator
from mlte.value.artifact import Value


class TestCase:
    """
    Class that contains all information about a test case.
    """

    def __init__(
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
        """Quality Attribute Scenario ids that are associated to this test case."""

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

    # -------------------------------------------------------------------------
    # Model conversion.
    # -------------------------------------------------------------------------

    def to_model(self) -> TestCaseModel:
        """
        Returns this test case as a model.

        :return: The serialized model object.
        """
        return TestCaseModel(
            name=self.name,
            goal=self.goal,
            qas_list=self.qas_list,
            measurement=(
                self.measurement.to_model() if self.measurement else None
            ),
            validator=self.validator.to_model() if self.validator else None,
        )

    @classmethod
    def from_model(cls, model: TestCaseModel) -> TestCase:
        """
        Deserialize a TestCase from a model.

        :param model: The model.

        :return: The deserialized TestCase
        """
        test_case: TestCase = TestCase(
            name=model.name,
            goal=model.goal,
            qas_list=model.qas_list,
            measurement=Measurement.from_model(model.measurement),
            validator=Validator.from_model(model.validator),
        )
        return test_case

    # -------------------------------------------------------------------------
    # Builtin overloads.
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of TestCase."""
        return f"{self.name}: {self.goal} ({self.qas_list})"

    def __eq__(self, other: object) -> bool:
        """Compare TestCase instances for equality."""
        if not isinstance(other, TestCase):
            return False
        reference: TestCase = other
        return self.to_model() == reference.to_model()
