"""
Unit tests for report schemas.
"""

import pytest
from jsonschema import ValidationError

from mlte.suites import Suite
from mlte.properties.costs import StorageCost

from mlte.measurement import bind
from mlte.measurement.utility import flatten
from mlte.measurement.storage import LocalObjectSize

from mlte.internal.schema import validate_suite_schema


def test_empty_instance():
    # Ensure that an empty report passes validation
    suite = Suite("MySuite")
    report = suite.collect()
    validate_suite_schema(report.document)


def test_instance_with_content():
    # Ensure that a report with content passes validation
    suite = Suite("MySuite", StorageCost())

    local_size = bind(
        LocalObjectSize().with_validator_size_not_greater_than(threshold=54000),
        suite.get_property("StorageCost"),
    )

    size_result = local_size.validate("test/")
    report = suite.collect(*flatten(size_result))

    validate_suite_schema(report.document)


def test_failure():
    # Test that an invalid suite fails validation
    suite = Suite("MySuite", StorageCost())

    local_size = bind(
        LocalObjectSize().with_validator_size_not_greater_than(threshold=54000),
        suite.get_property("StorageCost"),
    )

    size_result = local_size.validate("test/")
    report = suite.collect(*flatten(size_result))

    del report.document["name"]
    document = {}

    with pytest.raises(ValidationError):
        validate_suite_schema(document)
