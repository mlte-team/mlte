"""
test/value/types/test_opaque.py

Unit tests for Opaque.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.types.opaque import Opaque
from mlte.measurement.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa
from test.evidence.types.helper import get_sample_evidence_metadata


class DummyMeasurementOpaque(Measurement):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def __call__(self) -> Opaque:
        return Opaque({"value": 1}).with_metadata(self.evidence_metadata)


def test_measurement():
    """Opaque can be produced by a measurement."""

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


def test_equality():
    """Opaque instances can be compared for equality."""

    m = get_sample_evidence_metadata()

    a = Opaque({"foo": "bar"}).with_metadata(m)
    b = Opaque({"foo": "bar"}).with_metadata(m)
    assert a == b

    a = Opaque({"foo": [1, 2, 3]}).with_metadata(m)
    b = Opaque({"foo": [1, 2, 3]}).with_metadata(m)
    assert a == b

    a = Opaque({"foo": [1, 2, 3]}).with_metadata(m)
    b = Opaque({"foo": [3, 2, 1]}).with_metadata(m)
    assert a != b

    a = Opaque({"foo": {"bar": {"baz": 1}}}).with_metadata(m)
    b = Opaque({"foo": {"bar": {"baz": 2}}}).with_metadata(m)
    assert a != b


def test_serde() -> None:
    """Opaque can be converted to model and back."""
    o = Opaque({"value": 1}).with_metadata(get_sample_evidence_metadata())

    model = o.to_model()
    e = Opaque.from_model(model)

    assert e == o


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Opaque can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    o = Opaque({"foo": "bar"}).with_metadata(get_sample_evidence_metadata())
    o.save_with(ctx, store)

    loaded = Opaque.load_with("id.value", context=ctx, store=store)
    assert loaded == o
