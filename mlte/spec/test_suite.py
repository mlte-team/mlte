"""
TestSuite contains a collection of TestCases.
"""

from __future__ import annotations

import typing

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.spec.model import TestSuiteModel
from mlte.spec.spec import DEFAULT_SPEC_ID
from mlte.spec.test_case import TestCase


class TestSuite(Artifact):
    """
    The TestSuite contains a collection of TestCases to be
    measured and validated.
    """

    def __init__(
        self, identifier: str = DEFAULT_SPEC_ID, test_cases: list[TestCase] = []
    ):
        """
        Initialize a TestSuite instance.

        :param test_cases: The collection of test cases.
        """
        super().__init__(identifier, ArtifactType.SPEC)

        self.test_cases = test_cases
        """The collection of TestCases that compose the TestSuite."""

    def add_test_case(self, test_case: TestCase):
        """Adds a test case to its list."""
        self.test_cases.append(test_case)

    # -------------------------------------------------------------------------
    # Artifact overrides.
    # -------------------------------------------------------------------------

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_SPEC_ID

    # -------------------------------------------------------------------------
    # Model serialization.
    # -------------------------------------------------------------------------

    def to_model(self) -> ArtifactModel:
        """Convert a TestSuite artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=TestSuiteModel(
                test_cases=[
                    test_case.to_model() for test_case in self.test_cases
                ],
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> TestSuite:
        """Convert a TestSuite model to its corresponding artifact."""
        model = typing.cast(ArtifactModel, model)
        assert model.header.type == ArtifactType.SPEC, "Broken precondition."
        body = typing.cast(TestSuiteModel, model.body)
        return TestSuite(
            identifier=model.header.identifier,
            test_cases=[
                TestCase.from_model(test_case_model)
                for test_case_model in body.test_cases
            ],
        )

    # -------------------------------------------------------------------------
    # Builtin overloads.
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of TestCase."""
        return f"TestSuite contains {len(self.test_cases)} test cases"

    def __eq__(self, other: object) -> bool:
        """Compare TestSuite instances for equality."""
        if not isinstance(other, TestSuite):
            return False
        reference: TestSuite = other
        return self.to_model() == reference.to_model()
