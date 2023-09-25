"""
test/validation/test_specvalidator.py

Unit tests for SpecValidator functionality.
"""
from __future__ import annotations

import pytest

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.property.costs.storage_cost import StorageCost
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import SpecValidator
from mlte.value.types.integer import Integer


def test_no_property():
    # Spec validator does not have value for property.
    spec = Spec(
        properties={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_no_requirement():
    # Spec validator does not have value for condition.
    spec = Spec(
        properties={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)

    i = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id2")
        ),
        1,
    )
    specValidator.add_value(i)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_success():
    spec = Spec(
        properties={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)

    i = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="test")
        ),
        1,
    )
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    assert validatedSpec is not None
