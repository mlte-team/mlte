"""
TestCase defines structure for all tests to be defined for a TestSuite.
"""

from __future__ import annotations

import typing
from typing import Optional

from mlte.evidence.artifact import Evidence
from mlte.measurement.measurement import Measurement
from mlte.model.base_model import BaseModel
from mlte.model.serializable import Serializable
from mlte.results.result import Result
from mlte.tests.model import TestCaseModel
from mlte.validation.validator import Validator


class TestCase(Serializable):
    """
    Class that contains all information about a test case.
    """

    def __init__(
        self,
        identifier: str,
        goal: str,
        quality_scenarios: list[str],
        measurement: Optional[Measurement] = None,
        validator: Optional[Validator] = None,
    ):
        self.identifier = identifier
        """Unique id or name given to the test case."""

        self.goal = goal
        """Goal for the TestCase, reason for it."""

        self.quality_scenarios = quality_scenarios.copy()
        """Quality Attribute Scenario ids that are associated to this test case."""

        self.validator = validator
        """Used to validate this test case."""

        self.measurement = measurement
        """Used to measure and get a value for this test case."""

        if self.measurement:
            # If we got a Measurement, ensure its test case id matches ours.
            self.measurement.set_test_case_id(self.identifier)

    def measure(self, *args, **kwargs) -> Evidence:
        """Executes the configured measurement with the given params."""
        if self.measurement is None:
            raise RuntimeError(
                "Can't evaluate measurement, no measurement has been configured."
            )

        return self.measurement.evaluate(*args, **kwargs)

    def validate(self, evidence: Evidence) -> Result:
        """Executes the configured validator with the given Evidence."""
        if self.validator is None:
            raise RuntimeError(
                "Can't validate, no validator has been configured."
            )

        return self.validator.validate(evidence)._with_evidence_metadata(
            evidence.metadata
        )

    # -------------------------------------------------------------------------
    # Model conversion.
    # -------------------------------------------------------------------------

    def to_model(self) -> TestCaseModel:
        """
        Returns this test case as a model.

        :return: The serialized model object.
        """
        return TestCaseModel(
            identifier=self.identifier,
            goal=self.goal,
            qas_list=self.quality_scenarios,
            measurement=(
                self.measurement.generate_metadata()
                if self.measurement
                else None
            ),
            validator=self.validator.to_model() if self.validator else None,
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> TestCase:
        """
        Deserialize a TestCase from a model.

        :param model: The model.

        :return: The deserialized TestCase
        """
        model = typing.cast(TestCaseModel, model)
        test_case: TestCase = TestCase(
            identifier=model.identifier,
            goal=model.goal,
            quality_scenarios=model.qas_list,
            measurement=(
                Measurement.from_metadata(
                    model=model.measurement, test_case_id=model.identifier
                )
                if model.measurement
                else None
            ),
            validator=(
                Validator.from_model(model.validator)
                if model.validator
                else None
            ),
        )
        return test_case

    # -------------------------------------------------------------------------
    # Builtin overloads.
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of TestCase."""
        return f"{self.identifier}: {self.goal} ({self.quality_scenarios})"

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, TestCase):
            return False
        return self._equal(other)
