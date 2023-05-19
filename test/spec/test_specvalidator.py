"""
Unit tests for SpecValidator functionality.
"""

import pytest

from mlte.spec import Spec, Requirement, SpecValidator
from mlte.property.costs import StorageCost
from mlte.validation import Result
from mlte.value.types import Integer
from mlte.evidence import EvidenceMetadata
from mlte.measurement.storage import LocalObjectSize


def test_no_property():
    # Spec validator does not have value for property.
    spec = Spec(
        {StorageCost("rationale"): [Requirement("test", Integer.less_than(3))]}
    )
    specValidator = SpecValidator(spec)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_no_requirement():
    # Spec validator does not have value for requirement.
    spec = Spec(
        {StorageCost("rationale"): [Requirement("id", Integer.less_than(3))]}
    )
    specValidator = SpecValidator(spec)

    i = Integer(EvidenceMetadata("typename", "id2"), 1)
    specValidator.add_value(i)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_success():
    spec = Spec(
        {StorageCost("rationale"): [Requirement("id", Integer.less_than(3))]}
    )
    specValidator = SpecValidator(spec)

    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    assert validatedSpec is not None


def test_no_result():
    # Spec does not have value for requirement.
    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement("test", LocalObjectSize.value().less_than(3))
            ]
        }
    )
    specValidator = SpecValidator(spec)

    results: dict[str, Result] = {}
    with pytest.raises(RuntimeError):
        _ = specValidator._generate_validatedspec(results)
