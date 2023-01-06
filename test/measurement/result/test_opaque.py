"""
Unit tests for Opaque.
"""

import pytest

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


def test_opqaue_serde():
    m = MeasurementMetadata("typename", "identifier")
    o = Opaque(m, {"value": 1})

    serialized = o.serialize()
    recovered = Opaque.deserialize(m, serialized)

    assert "value" in recovered.data
    assert recovered["value"] == o["value"]
