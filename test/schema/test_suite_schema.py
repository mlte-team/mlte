"""
Unit tests for report schemas.
"""

import pytest
from jsonschema import ValidationError

from mlte.spec import Spec
from mlte.property.costs import StorageCost

from mlte.measurement.utility import flatten
from mlte.measurement.storage import LocalObjectSize

from mlte._private.schema import validate_spec_schema


def test_empty_instance():
    # Ensure that an empty report passes validation
    spec = Spec("MySpec")
    report = spec.collect()
    validate_spec_schema(report.document)


# TODO(Kyle): Fix to make functional
@pytest.mark.skip()
def test_instance_with_content():
    # Ensure that a report with content passes validation
    spec = Spec("MySpec", StorageCost())

    local_size = LocalObjectSize()

    size_result = local_size.validate("test/")
    report = spec.collect(*flatten(size_result))

    validate_spec_schema(report.document)


# TODO(Kyle): Fix to make functional
@pytest.mark.skip()
def test_failure():
    # Test that an invalid spec fails validation
    spec = Spec("MySpec", StorageCost())

    local_size = LocalObjectSize()

    size_result = local_size.validate("test/")
    report = spec.collect(*flatten(size_result))

    # Remove a required field
    del report.document["name"]

    with pytest.raises(ValidationError):
        validate_spec_schema(report.document)
