"""
TestResults class implementation.
"""

from __future__ import annotations

import typing
from typing import Optional, Type, Union

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.results.model import TestResultsModel
from mlte.results.result import Failure, Info, Result, Success
from mlte.suite.model import TestSuiteModel
from mlte.suite.test_case import TestCase
from mlte.suite.test_suite import TestSuite

# -----------------------------------------------------------------------------
# TestResults
# -----------------------------------------------------------------------------


class TestResults(Artifact):
    """
    TestResults represents a the results for a TestSuite.
    """

    type = ArtifactType.TEST_RESULTS
    """Class attribute indicating type."""

    def __init__(
        self,
        test_suite: TestSuite,
        identifier: Optional[str] = None,
        results: dict[str, Result] = {},
    ):
        """
        Initialize a TestResults instance.

        :param identifier: An id for this set of test results.
        :param test_suite: The TestSuite
        :param results: The validation Results for the TestSuite
        """
        super().__init__(identifier)

        self.test_suite = test_suite
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
                test_suite_id=self.test_suite.identifier,
                test_suite=typing.cast(
                    TestSuiteModel, self.test_suite.to_model().body
                ),
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
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.TEST_RESULTS
        ), "Type should be TestResults."
        body = typing.cast(TestResultsModel, model.body)

        # Build the TestSuite and TestResults
        return TestResults(
            identifier=model.header.identifier,
            test_suite=TestSuite(
                identifier=body.test_suite_id,
                test_cases=[
                    TestCase.from_model(test_case_model)
                    for test_case_model in body.test_suite.test_cases
                ],
            ),
            results={
                test_case_id: Result.from_model(test_result_model)
                for test_case_id, test_result_model in body.results.items()
            },
        )

    # Overriden.
    @classmethod
    def load(cls, identifier: typing.Optional[str] = None) -> TestResults:
        """
        Load a TestResults from the configured global session.
        :param identifier: The identifier for the artifact. If None,
        the default id is used.
        """
        suite = super().load(identifier)
        return typing.cast(TestResults, suite)

    # -------------------------------------------------------------------------
    # Helpers.
    # -------------------------------------------------------------------------

    def print_results(self, result_type: str = "all"):
        """Prints the validated results per test case, can be filtered by result type."""
        if result_type not in ["all", "Success", "Failure", "Info"]:
            raise RuntimeError(f"Invalid type: {result_type}")

        for test_case_id, result in self.results.items():
            if result_type == "all" or result_type == str(result):
                print(
                    f" > Test Case: {test_case_id}, result: {result}, details: {result.message}"
                )

    def convert_result(
        self,
        test_case_id: str,
        result_type: Union[Type[Success], Type[Failure]],
        message: str,
    ) -> None:
        """Converts a given Info result into the provided type."""
        if test_case_id not in self.results:
            raise RuntimeError(
                f"Test case {test_case_id} is not in the list of results."
            )

        result = self.results[test_case_id]
        if not isinstance(result, Info):
            raise RuntimeError(
                "Only results of type Info can be manually validated."
            )

        # Create new result based on given type.
        new_result_msg = f"Manually validated: {message} (original message: {result.message})"
        new_result = result_type(new_result_msg)
        self.results[test_case_id] = new_result

    # -------------------------------------------------------------------------
    # Default overriden.
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Test TestResults instance for equality."""
        if not isinstance(other, TestResults):
            return False
        return self._equal(other)
