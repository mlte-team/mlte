"""
Class in charge of validating a TestSuite.
"""

from __future__ import annotations

from mlte.evidence.artifact import Evidence
from mlte.spec.test_suite import TestSuite
from mlte.validation.result import Result
from mlte.validation.test_results import TestResults

# -----------------------------------------------------------------------------
# TestSuiteValidator
# -----------------------------------------------------------------------------


class TestSuiteValidator:
    """
    Helper class to validate a test suite.
    """

    def __init__(self, test_suite: TestSuite):
        """
        Initialize a TestSuiteValidator instance.

        :param test_suite: The test suite to be validated
        """

        self.test_suite = test_suite
        """The specification to be validated."""

        self.values: dict[str, Evidence] = {}
        """Where values will be gathered for validation."""

    def add_values(self, values: list[Evidence]):
        """
        Adds multiple values.

        :param values: The list of values to add to the internal list.
        """
        for value in values:
            self.add_value(value)

    def add_value(self, value: Evidence):
        """
        Adds a value associated to a test case.

        :param value: The value to add to the internal list.
        """
        if value.metadata.test_case_id in self.values:
            raise RuntimeError(
                f"Can't have two values with the same id: {value.metadata.test_case_id}"
            )
        self.values[value.metadata.test_case_id] = value

    def validate(self) -> TestResults:
        """
        Validates the internal Values given its validators, and generates a TestResults from it.

        :return: The results of the test validation.
        """
        # Check that all conditions have values to be validated.
        for test_case_id in self.test_suite.test_cases.keys():
            if test_case_id not in self.values:
                raise RuntimeError(
                    f"Test Case '{test_case_id}' does not have a value that can be validated."
                )

        # Validate and aggregate the results.
        results: dict[str, Result] = {}
        for test_case_id, test_case in self.test_suite.test_cases.items():
            results[test_case_id] = test_case.validate(
                self.values[test_case_id]
            )

        return TestResults(test_suite=self.test_suite, results=results)
