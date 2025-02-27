"""
TestResults class implementation.
"""

from __future__ import annotations

import typing
from typing import Optional

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.spec.test_suite import TestSuite
from mlte.validation.model import TestResultsModel
from mlte.validation.result import Result

DEFAULT_VALIDATED_SPEC_ID = "default.validated_spec"

# -----------------------------------------------------------------------------
# TestResults
# -----------------------------------------------------------------------------


class TestResults(Artifact):
    """
    TestResults represents a the results for a TestSuite.
    """

    def __init__(
        self,
        identifier: str = DEFAULT_VALIDATED_SPEC_ID,
        test_suite: Optional[TestSuite] = None,
        results: dict[str, Result] = {},
    ):
        """
        Initialize a TestResults instance.

        :param identifier: An id for this set of test results.
        :param test_suite: The TestSuite
        :param results: The validation Results for the TestSuite
        """
        super().__init__(identifier, ArtifactType.TEST_RESULTS)

        self.test_suite_id = (
            test_suite.identifier if test_suite is not None else ""
        )
        """The id of the TestSuite that we validated."""

        self.results = results
        """The validation results for the test_suite, by test case."""

        # Check that all tests have results.
        if test_suite:
            for test_case_id, _ in test_suite.test_cases.items():
                if test_case_id not in results:
                    raise RuntimeError(
                        f"Test Case '{test_case_id}' does not have a result."
                    )

    # -------------------------------------------------------------------------
    # Model serialization.
    # -------------------------------------------------------------------------

    def to_model(self) -> ArtifactModel:
        """
        Generates a model representation of the TestResults.
        :return: The serialized model
        """
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=TestResultsModel(
                test_suite_id=self.test_suite_id,
                results={
                    test_case_id: result.to_model()
                    for test_case_id, result in self.results.items()
                },
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> TestResults:
        """
        Deserialize TestResults content from model.
        :param model: The model
        :return: The deserialized specification
        """
        model = typing.cast(ArtifactModel, model)
        assert (
            model.header.type == ArtifactType.TEST_RESULTS
        ), "Broken precondition."
        body = typing.cast(TestResultsModel, model.body)

        # Build the TestSuite and TestResults
        return TestResults(
            identifier=model.header.identifier,
            test_suite_id=body.test_suite_id,
            results={
                test_case_id: Result.from_model(test_result_model)
                for test_case_id, test_result_model in body.results.items()
            },
        )

    # -------------------------------------------------------------------------
    # Helpers.
    # -------------------------------------------------------------------------

    def print_results(self, result_type: str = "all"):
        """Prints the validated results per property, can be filtered by result type."""
        if result_type not in ["all", "Success", "Failure", "Info"]:
            raise RuntimeError(f"Invalid type: {result_type}")

        for test_case_id, result in self.results.items():
            if result_type == "all" or result_type == str(result):
                print(
                    f" > Test Case: {test_case_id}, result: {result}, details: {result.message}"
                )

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_VALIDATED_SPEC_ID

    def __eq__(self, other: object) -> bool:
        """Test TestResults instance for equality."""
        if not isinstance(other, TestResults):
            return False
        return self._equal(other)
