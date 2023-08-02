"""
test/spec/test_specvalidator.py

Unit tests for SpecValidator functionality.
"""
from __future__ import annotations

import pytest

from mlte.evidence import EvidenceMetadata
from mlte.property.costs import StorageCost
from mlte.spec import Requirement, Spec, SpecValidator
from mlte.value.types import Integer


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
