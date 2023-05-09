"""
Unit tests for SpecValidator functionality.
"""

import pytest

from mlte.spec import Spec, Requirement, SpecValidator
from mlte.property.costs import StorageCost
from mlte.measurement import ExternalMeasurement

from mlte.value.types import Integer
from mlte.evidence import EvidenceMetadata


def test_no_property():
    # Spec validator does not have value for property.
    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement(
                    "test", ExternalMeasurement.__name__, "less_than", 3
                )
            ]
        }
    )
    specValidator = SpecValidator(spec)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_no_requirement():
    # Spec validator does not have value for requirement.
    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement(
                    "test", ExternalMeasurement.__name__, "less_than", 3
                )
            ]
        }
    )
    specValidator = SpecValidator(spec)

    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value("StorageCost", "test2", i)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_success():
    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement(
                    "test", ExternalMeasurement.__name__, "less_than", 3
                )
            ]
        }
    )
    specValidator = SpecValidator(spec)

    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value("StorageCost", "test", i)

    validatedSpec = specValidator.validate()
    assert validatedSpec is not None
