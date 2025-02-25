"""
test/validation/test_specvalidator.py

Unit tests for SpecValidator functionality.
"""

from __future__ import annotations

import pytest

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.evidence.types.integer import Integer
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import TestSuiteValidator


def test_no_qa_category():
    # Spec validator does not have value for quality attribute_category.
    spec = Spec(
        qa_categories={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = TestSuiteValidator(spec)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_no_requirement():
    # Spec validator does not have value for condition.
    spec = Spec(
        qa_categories={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = TestSuiteValidator(spec)

    i = Integer(
        EvidenceMetadata(
            measurement_class="typename", test_case_id=Identifier(name="id2")
        ),
        1,
    )
    specValidator.add_value(i)

    with pytest.raises(RuntimeError):
        _ = specValidator.validate()


def test_success():
    spec = Spec(
        qa_categories={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = TestSuiteValidator(spec)

    i = Integer(
        EvidenceMetadata(
            measurement_class="typename", test_case_id=Identifier(name="test")
        ),
        1,
    )
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    assert validatedSpec is not None
