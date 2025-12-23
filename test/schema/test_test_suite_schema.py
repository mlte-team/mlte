"""
Unit tests for TestSuite schema.
"""

from mlte.suite.test_case import TestCase
from mlte.suite.test_suite import TestSuite

from . import util as util


def test_instance_with_content():
    test_suite = TestSuite(
        test_cases=[
            TestCase(identifier="test", goal="test", quality_scenarios=[])
        ]
    )

    doc = test_suite.to_model().to_json()
    util.validate_test_suite_schema(doc["body"])
