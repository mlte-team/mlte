"""
test/measurement/test_external_measurement.py

Unit test for ExternalMeasurement.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement import ExternalMeasurement
from mlte.value.base import ValueBase
from mlte.value.types.integer import Integer


class BigInteger(ValueBase):
    """A sample extension value type."""

    def __init__(self, metadata: EvidenceMetadata, integer: int):
        super().__init__(self, metadata)
        self.integer = integer

    def serialize(self) -> Dict[str, Any]:
        return {"integer": self.integer}

    @staticmethod
    def deserialize(
        metadata: EvidenceMetadata, data: Dict[str, Any]
    ) -> BigInteger:
        return BigInteger(metadata, data["integer"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BigInteger):
            return False
        return self.integer == other.integer


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


def test_evaluate_external() -> None:
    """An external measurement can be evaluated to a MLTE builtin."""

    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = Integer(
        EvidenceMetadata(
            measurement_type="dummy", identifier=Identifier(name="test")
        ),
        expected_value,
    )

    measurement = ExternalMeasurement("dummy", Integer, _dummy_calculation)
    result = measurement.evaluate(x, y)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_external_base() -> None:
    """An external measurement can be evaluated to a MLTE value extension."""

    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = BigInteger(
        EvidenceMetadata(
            measurement_type="dummy", identifier=Identifier(name="test")
        ),
        expected_value,
    )

    measurement = ExternalMeasurement("dummy", BigInteger, _dummy_calculation)
    result = measurement.evaluate(x, y)

    assert isinstance(result, BigInteger)
    assert result == expected_result


def test_evaluate_ingest() -> None:
    """An external measurement can be used to ingest a value directly."""

    expected_value = 1000
    expected_result = Integer(
        EvidenceMetadata(
            measurement_type="dummy", identifier=Identifier(name="test")
        ),
        expected_value,
    )

    measurement = ExternalMeasurement("dummy", Integer)
    result = measurement.ingest(expected_value)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_ingest_base() -> None:
    """An external measurement can be used to ingest an extension value."""

    expected_value = 1000
    expected_result = BigInteger(
        EvidenceMetadata(
            measurement_type="dummy", identifier=Identifier(name="test")
        ),
        expected_value,
    )

    measurement = ExternalMeasurement("dummy", BigInteger)
    result = measurement.ingest(expected_value)

    assert isinstance(result, BigInteger)
    assert result == expected_result


def test_invalid_result_type() -> None:
    """An external measurement cannot be instantiated with a bad result type."""

    with pytest.raises(Exception):
        _ = ExternalMeasurement("dummy", int)


def test_invalid_function() -> None:
    """An external measurement cannot be instantiated with a bad function type."""

    with pytest.raises(Exception):
        ExternalMeasurement("dummy", Integer, "not_a_function")


def test_evaluate_no_function() -> None:
    """An external measurement cannot be evaluated with no function."""

    x = 1
    y = 2

    measurement = ExternalMeasurement("dummy", Integer)
    with pytest.raises(Exception):
        measurement.evaluate(x, y)
