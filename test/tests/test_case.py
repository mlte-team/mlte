"""
Unit tests for TestCase functionality.
"""

from __future__ import annotations

from mlte.evidence.types.integer import Integer
from mlte.results.result import Failure, Success
from mlte.tests.test_case import TestCase
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata


def get_sample_test_case():
    test_case = TestCase(identifier="t1", goal="to test", qas_list=["qa1"])
    return test_case


def test_round_trip() -> None:
    """TestCase can be converted to model and back."""
    test_case = get_sample_test_case()

    model = test_case.to_model()
    loaded = TestCase.from_model(model)

    assert test_case == loaded


def test_validate():
    """Checks that validation can be done properly through a TestCase."""
    test_case = get_sample_test_case()
    test_case.validator = Validator(
        bool_exp=lambda x: x.value < 1, success="Yay", failure="oh"
    )
    ev1 = Integer(0).with_metadata(
        get_sample_evidence_metadata(test_case_id=test_case.identifier)
    )
    ev2 = Integer(1).with_metadata(
        get_sample_evidence_metadata(test_case_id=test_case.identifier)
    )

    result1 = test_case.validate(ev1)
    assert isinstance(result1, Success)
    assert result1.evidence_metadata is not None
    assert result1.evidence_metadata.test_case_id == test_case.identifier

    result2 = test_case.validate(ev2)
    assert isinstance(result2, Failure)
    assert result2.evidence_metadata is not None
    assert result2.evidence_metadata.test_case_id == test_case.identifier
