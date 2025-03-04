"""
Unit tests for TestSuite schema.
"""

from mlte.spec.test_case import TestCase
from mlte.spec.test_suite import TestSuite

from . import util as util


def test_instance_with_content():
    spec = TestSuite(
        test_cases=[TestCase(identifier="test", goal="test", qas_list=[])]
    )

    doc = spec.to_model().to_json()
    util.validate_spec_schema(doc["body"])
