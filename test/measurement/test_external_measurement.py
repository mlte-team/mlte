"""
Unit test for ExternalMeasurement.
"""
import pytest

from mlte.evidence.evidence_metadata import EvidenceMetadata
from mlte.measurement import ExternalMeasurement
from mlte.value.types import Integer


def _dummy_calculation(x: int, y: int):
    """
    Dummy calculation function that adds two ints and multiplies the result by two.

    :param x: The first number
    :type x: int
    :param y: The second number
    :type y: int

    :return: the result of the calculation
    :rtype: int
    """
    return (x + y) * 2


def test_evaluate_external():
    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = Integer(EvidenceMetadata("dummy", "test"), expected_value)

    measurement = ExternalMeasurement("dummy", Integer)
    result = measurement.evaluate(_dummy_calculation(x, y))

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_ingest():
    expected_value = 1000
    expected_result = Integer(EvidenceMetadata("dummy", "test"), expected_value)

    measurement = ExternalMeasurement("dummy", Integer)
    result = measurement.ingest(expected_value)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_invalid_result_type():
    with pytest.raises(Exception):
        ExternalMeasurement("dummy", int)
