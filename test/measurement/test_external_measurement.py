"""
test/measurement/test_external_measurement.py

Unit test for ExternalMeasurement.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from mlte.evidence.external import ExternalEvidence
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.types.integer import Integer
from mlte.measurement.external_measurement import ExternalMeasurement
from mlte.measurement.model import MeasurementMetadata


class BigInteger(ExternalEvidence):
    """A sample extension value type."""

    def __init__(self, integer: int):
        self.integer = integer

    def serialize(self) -> Dict[str, Any]:
        return {"integer": self.integer}

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> BigInteger:
        return BigInteger(data["integer"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BigInteger):
            return False
        return self._equal(other)


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


def get_sample_metadata() -> EvidenceMetadata:
    """Sample for tests."""
    return EvidenceMetadata(
        measurement=MeasurementMetadata(
            measurement_class="mlte.measurement.external_measurement.ExternalMeasurement",
            output_class="BigInt",
            additional_data={
                ExternalMeasurement.EXTERNAL_FUNCTION_KEY: "test.measurement.test_external_measurement._dummy_calculation"
            },
        ),
        test_case_id="test_id",
    )


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = ExternalMeasurement("test_id", Integer)

    assert (
        m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.external_measurement.ExternalMeasurement"
    )


def test_evaluate_external() -> None:
    """An external measurement can be evaluated to a MLTE builtin."""

    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = Integer(expected_value).with_metadata(
        get_sample_metadata()
    )

    measurement = ExternalMeasurement("test_id", Integer, _dummy_calculation)
    result = measurement.evaluate(x, y)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_external_base() -> None:
    """An external measurement can be evaluated to a MLTE value extension."""

    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = BigInteger(expected_value).with_metadata(
        get_sample_metadata()
    )

    measurement = ExternalMeasurement("test_id", BigInteger, _dummy_calculation)
    result = measurement.evaluate(x, y)

    assert isinstance(result, BigInteger)
    print(result.to_model())
    print(expected_result.to_model())
    assert result == expected_result


def test_evaluate_ingest() -> None:
    """An external measurement can be used to ingest a value directly."""

    expected_value = 1000
    expected_result = Integer(expected_value).with_metadata(
        get_sample_metadata()
    )

    measurement = ExternalMeasurement("test_id", Integer)
    result = measurement.ingest(expected_value)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_ingest_base() -> None:
    """An external measurement can be used to ingest an extension value."""

    expected_value = 1000
    expected_result = BigInteger(expected_value).with_metadata(
        get_sample_metadata()
    )

    measurement = ExternalMeasurement("test_id", BigInteger)
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
        ExternalMeasurement("dummy", Integer, "not_a_function")  # type: ignore


def test_evaluate_no_function() -> None:
    """An external measurement cannot be evaluated with no function."""

    x = 1
    y = 2

    measurement = ExternalMeasurement("dummy", Integer)
    with pytest.raises(Exception):
        measurement.evaluate(x, y)
