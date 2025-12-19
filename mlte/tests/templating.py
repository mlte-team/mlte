"""Template generator for TestSuite from system requirements."""

from mlte.negotiation.qas import QASDescriptor
from mlte.tests.test_case import TestCase
from mlte.tests.test_suite import TestSuite


def generate_suite_str(requirements: list[QASDescriptor]) -> str:
    """
    Generate a TestSuite template string from a list of requirements.

    :param requirements: List of system requirements to make into TestCases
    :return: TestSuite template string that can be used to instantiate a TestSuite
    """
    suite = TestSuite()
    for requirement in requirements:
        suite.add_test_case(
            TestCase(
                identifier=str(requirements.index(requirement) + 1),
                goal="",
                quality_scenarios=[
                    requirement.identifier if requirement.identifier else ""
                ],
            )
        )

    return suite.to_template_str()
