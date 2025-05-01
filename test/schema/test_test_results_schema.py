"""
Unit tests for TestResults schema.
"""

from mlte.artifact.type import ArtifactType
from mlte.evidence.types.integer import Integer
from mlte.tests.test_suite import TestSuite
from mlte.validation.test_suite_validator import TestSuiteValidator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.fixture.artifact import ArtifactFactory

from . import util as util


def test_schema():
    test_suite = TestSuite.from_model(
        ArtifactFactory.make(ArtifactType.TEST_SUITE)
    )
    test_suite_validator = TestSuiteValidator(test_suite)
    i = Integer(1).with_metadata(
        get_sample_evidence_metadata(test_case_id="Test1")
    )
    test_suite_validator.add_evidence(i)
    test_results = test_suite_validator.validate()

    doc = test_results.to_model().to_json()
    util.validate_test_results_schema(doc["body"])
