"""
Unit tests for Opaque.
"""

import pytest

import mlte
from mlte.measurement import Measurement, MeasurementMetadata
from mlte.measurement.result import Opaque


class DummyMeasurementOpaque(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Opaque:
        return Opaque(self.metadata, {"value": 1})


def test_opaque():
    m = DummyMeasurementOpaque("identifier")
    t = m.evaluate()
    assert isinstance(t, Opaque)

    assert "value" in t.data
    assert t.data["value"] == 1

    # Opaque is subscriptable, like a dictionary
    assert t["value"] == t.data["value"]

    # Opaque raises for invalid key
    with pytest.raises(KeyError):
        _ = t["foo"]

    # Opaque is read-only
    with pytest.raises(ValueError):
        t["value"] = 2  # type: ignore


def test_opaque_equality():
    m = MeasurementMetadata("typename", "identifier")

    a = Opaque(m, {"foo": "bar"})
    b = Opaque(m, {"foo": "bar"})
    assert a == b

    a = Opaque(m, {"foo": [1, 2, 3]})
    b = Opaque(m, {"foo": [1, 2, 3]})
    assert a == b

    a = Opaque(m, {"foo": [1, 2, 3]})
    b = Opaque(m, {"foo": [3, 2, 1]})
    assert a != b

    a = Opaque(m, {"foo": {"bar": {"baz": 1}}})
    b = Opaque(m, {"foo": {"bar": {"baz": 2}}})
    assert a != b


def test_opaque_save_load(tmp_path):
    mlte.set_model("mymodel", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    m = MeasurementMetadata("typename", "identifier")
    i = Opaque(m, {"foo": "bar"})

    # Save
    i.save()

    # Recover
    r = Opaque.load("identifier")

    assert r == i


def test_opqaue_serde():
    m = MeasurementMetadata("typename", "identifier")
    o = Opaque(m, {"value": 1})

    serialized = o.serialize()
    recovered = Opaque.deserialize(m, serialized)

    assert "value" in recovered.data
    assert recovered["value"] == o["value"]
