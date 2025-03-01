"""
Unit tests for TestResults schema.
"""

from mlte.evidence.types.integer import Integer
from mlte.spec.test_suite import TestSuite
from mlte.validation.test_suite_validator import TestSuiteValidator
from test.fixture.artifact import make_complete_test_suite_model
from test.value.types.helper import get_sample_evidence_metadata

from . import util as util


def test_schema():
    test_suite = TestSuite.from_model(make_complete_test_suite_model())
    test_suite_validator = TestSuiteValidator(test_suite)
    i = Integer(1).with_metadata(
        get_sample_evidence_metadata(test_case_id="Test1")
    )
    test_suite_validator.add_value(i)
    test_results = test_suite_validator.validate()

    doc = test_results.to_model().to_json()
    util.validate_validatedspec_schema(doc["body"])
