"""
Unit tests for Real.
"""

import pytest

import mlte
from mlte.measurement import Measurement, MeasurementMetadata
from mlte.measurement.result import Real


class DummyMeasurementReal(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Real:
        return Real(self.metadata, 3.14)


def test_real_success():
    # Ensure instantiation succeeds for valid type
    m = MeasurementMetadata("typename", "identifier")
    r = Real(m, 3.14)
    assert r.value == 3.14


def test_real_fail():
    m = MeasurementMetadata("typename", "identifier")
    with pytest.raises(AssertionError):
        _ = Real(m, 1)


def test_real_serde():
    # Ensure serialization and deserialization are inverses
    m = MeasurementMetadata("typename", "identifier")
    r = Real(m, 3.14)

    serialized = r.serialize()
    recovered = Real.deserialize(m, serialized)
    assert recovered == r


def test_real_save_load(tmp_path):
    mlte.set_model("mymodel", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    m = MeasurementMetadata("typename", "identifier")
    i = Real(m, 3.14)

    # Save
    i.save()

    # Recover
    r = Real.load("identifier")

    assert r == i


def test_real_e2e():
    m = DummyMeasurementReal("identifier")
    r = m.evaluate()
    assert isinstance(r, Real)
    assert r.value == 3.14
