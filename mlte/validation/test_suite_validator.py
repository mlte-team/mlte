"""
Class in charge of validating a TestSuite.
"""

from __future__ import annotations

from typing import Optional

from mlte.evidence.artifact import Evidence
from mlte.results.result import Result
from mlte.results.test_results import TestResults
from mlte.tests.test_suite import TestSuite

# -----------------------------------------------------------------------------
# TestSuiteValidator
# -----------------------------------------------------------------------------


class TestSuiteValidator:
    """
    Helper class to validate a test suite.
    """

    def __init__(
        self, test_suite: Optional[TestSuite] = None, test_suite_id: str = ""
    ):
        """
        Initialize a TestSuiteValidator instance.

        :param test_suite: The test suite to be validated
        """

        # If no test suite is provided, load it from its id or its default one.
        if test_suite is None:
            if test_suite_id != "":
                test_suite = TestSuite.load(test_suite_id)
            else:
                test_suite = TestSuite.load()

        self.test_suite = test_suite
        """The test suite to be validated."""

        self.evidence: dict[str, Evidence] = {}
        """Where evidence will be gathered for validation."""

    def add_evidence_list(self, evidence_list: list[Evidence]):
        """
        Adds multiple evidence values.

        :param evidence_list: The list of evidence to add to the internal list.
        """
        for evidence in evidence_list:
            self.add_evidence(evidence)

    def add_evidence(self, evidence: Evidence):
        """
        Adds Evidence associated to a test case.

        :param evidence: The evidence to add to the internal list.
        """
        if not evidence.metadata:
            raise RuntimeError("Provided evidence has no metadata.")

        if evidence.metadata.test_case_id in self.evidence:
            raise RuntimeError(
                f"Can't have two values with the same id: {evidence.metadata.test_case_id}"
            )
        self.evidence[evidence.metadata.test_case_id] = evidence

    def load_and_validate(self) -> TestResults:
        """Loads all Evidence for the model/context and store in session, and validates."""
        self.add_evidence_list(Evidence.load_all())
        return self.validate()

    def validate(self) -> TestResults:
        """
        Validates the internal Evidence given its validators, and generates a TestResults from it.

        :return: The results of the test validation.
        """
        # Check that all test cases have evidence to be validated.
        for test_case_id in self.test_suite.test_cases.keys():
            if test_case_id not in self.evidence:
                raise RuntimeError(
                    f"Test Case '{test_case_id}' does not have evidence that can be validated."
                )

        # Validate and aggregate the results.
        results: dict[str, Result] = {}
        for test_case_id, test_case in self.test_suite.test_cases.items():
            results[test_case_id] = test_case.validate(
                self.evidence[test_case_id]
            )

        return TestResults(test_suite=self.test_suite, results=results)
