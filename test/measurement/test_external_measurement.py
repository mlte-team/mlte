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
from mlte.measurement.measurement import Measurement
from mlte.measurement.model import MeasurementMetadata
from mlte.measurement.units import Unit, Units


class BigInteger(ExternalEvidence):
    """A sample extension value type."""

    def __init__(self, integer: int):
        super().__init__()
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


def _dummy_calculation(x: int, y: int) -> int:
    """
    Dummy calculation function that adds two ints and multiplies the result by two.
    """
    return (x + y) * 2


def _tuple_calculation(x: int, y: int) -> tuple[int, Unit]:
    """
    Dummy calculation function that just returns the numbers multiplied by each other, and a unit.
    """
    return x * y, Units.kilogram


def get_sample_metadata(
    additional_data: bool = True,
    output_class: str = "test.measurement.test_external_measurement.BigInteger",
    function: str = "test.measurement.test_external_measurement._dummy_calculation",
) -> EvidenceMetadata:
    """Sample for tests."""
    evidence = EvidenceMetadata(
        measurement=MeasurementMetadata(
            measurement_class="mlte.measurement.external_measurement.ExternalMeasurement",
            output_class=output_class,
        ),
        test_case_id="test_id",
    )
    if additional_data:
        evidence.measurement.additional_data[
            ExternalMeasurement.EXTERNAL_FUNCTION_KEY
        ] = function
    return evidence


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = ExternalMeasurement("test_id", Integer, function=get_sample_metadata)

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.external_measurement.ExternalMeasurement"
        and m.function == get_sample_metadata
    )
    assert m.output_evidence_type == Integer


def test_load_from_metadata():
    """ "Checks that we can generate and load measurement metadata."""
    m = ExternalMeasurement("test_id", Integer, get_sample_metadata)
    metadata = m.generate_metadata()

    m2 = Measurement.from_metadata(metadata, test_case_id="test_id")
    assert m == m2


def test_evaluate_external() -> None:
    """An external measurement can be evaluated to a MLTE builtin."""

    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = Integer(expected_value).with_metadata(
        get_sample_metadata(output_class="mlte.evidence.types.integer.Integer")
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
    assert result == expected_result


def test_evaluate_ingest() -> None:
    """An external measurement can be used to ingest a value directly."""

    expected_value = 1000
    expected_result = Integer(expected_value).with_metadata(
        get_sample_metadata(
            additional_data=False,
            output_class="mlte.evidence.types.integer.Integer",
        )
    )

    measurement = ExternalMeasurement("test_id", Integer)
    result = measurement.evaluate(expected_value)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_ingest_base() -> None:
    """An external measurement can be used to ingest an extension value."""

    expected_value = 1000
    expected_result = BigInteger(expected_value).with_metadata(
        get_sample_metadata(additional_data=False)
    )

    measurement = ExternalMeasurement("test_id", BigInteger)
    result = measurement.evaluate(expected_value)

    assert isinstance(result, BigInteger)
    assert result == expected_result


def test_evaluate_tuple() -> None:
    """An external measurement can be evaluated when the function returns a tuple."""

    x = 1
    y = 2
    expected_value, expected_unit = _tuple_calculation(x, y)
    expected_result = Integer(expected_value, expected_unit).with_metadata(
        get_sample_metadata(
            output_class="mlte.evidence.types.integer.Integer",
            function="test.measurement.test_external_measurement._tuple_calculation",
        )
    )

    measurement = ExternalMeasurement("test_id", Integer, _tuple_calculation)
    result = measurement.evaluate(x, y)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_invalid_result_type() -> None:
    """An external measurement cannot be instantiated with a bad result type."""

    with pytest.raises(Exception):
        _ = ExternalMeasurement("dummy", int)  # type: ignore


def test_invalid_function() -> None:
    """An external measurement cannot be instantiated with a bad function type."""

    with pytest.raises(Exception):
        ExternalMeasurement("dummy", Integer, "not_a_function")  # type: ignore


def test_evaluate_invalid_args() -> None:
    """An external measurement with invalid number of args throws an exception."""
    x = 1

    measurement = ExternalMeasurement("dummy", Integer, _dummy_calculation)

    with pytest.raises(Exception):
        _ = measurement.evaluate(x)

    with pytest.raises(Exception):
        _ = measurement.evaluate(x, x, x)
