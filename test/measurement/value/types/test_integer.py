"""
Unit tests for Integer.
"""

import pytest

import mlte
from mlte.measurement import Measurement
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata
from mlte.value.types import Integer


class DummyMeasurementInteger(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Integer:
        return Integer(self.metadata, 1)


def test_integer_success():
    # Ensure instantiation succeeds for valid type
    m = MeasurementMetadata("typename", "id")
    i = Integer(m, 1)
    assert i.value == 1


def test_integer_fail():
    # Ensure instantiation fails for invalid type
    m = MeasurementMetadata("typename", "id")
    with pytest.raises(AssertionError):
        _ = Integer(m, 3.14)  # type: ignore


def test_integer_serde():
    # Ensure serialization and deserialization are inverses
    m = MeasurementMetadata("typename", "id")
    i = Integer(m, 1)

    serialized = i.serialize()
    recovered = Integer.deserialize(m, serialized)
    assert recovered == i


def test_integer_save_load(tmp_path):
    mlte.set_model("mymodel", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    m = MeasurementMetadata("typename", "id")
    i = Integer(m, 1)

    # Save
    i.save()

    # Recover
    r = Integer.load("id")

    assert r == i


def test_integer_e2e():
    m = DummyMeasurementInteger("identifier")
    i = m.evaluate()
    assert isinstance(i, Integer)
    assert i.value == 1
