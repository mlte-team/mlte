"""
Unit tests for MeasurementToken.
"""

from mlte.measurement import MeasurementToken


def test_equality():
    a = MeasurementToken("Test")
    b = a
    assert a == b


def test_inequality():
    a = MeasurementToken("Test")
    b = MeasurementToken("Test")
    assert a != b
