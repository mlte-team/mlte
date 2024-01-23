"""
test/value/types/test_opaque.py

Unit tests for Opaque.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from mlte.value.types.opaque import Opaque

from ...fixture.store import store_with_context  # noqa


class DummyMeasurementOpaque(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Opaque:
        return Opaque(self.metadata, {"value": 1})


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

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )

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


def test_serde() -> None:
    """Opaque can be converted to model and back."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    o = Opaque(m, {"value": 1})

    model = o.to_model()
    e = Opaque.from_model(model)

    assert e == o


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Opaque can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    o = Opaque(m, {"foo": "bar"})
    o.save_with(ctx, store)

    loaded = Opaque.load_with("id.value", context=ctx, store=store)
    assert loaded == o
