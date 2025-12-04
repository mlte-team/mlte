"""
Unit tests for String.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.types.string import String
from mlte.measurement.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa


class DummyMeasurementString(Measurement):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def __call__(self) -> String:
        return String("test")


def test_success():
    """String construction works for valid input type."""
    i = String("test").with_metadata(get_sample_evidence_metadata())
    assert i.value == "test"


def test_fail():
    """String construction fails for invalid input type."""

    with pytest.raises(AssertionError):
        _ = String(3.14).with_metadata(get_sample_evidence_metadata())  # type: ignore


def test_measurement():
    """String can be produced by measurement."""

    m = DummyMeasurementString("identifier")
    i = m.evaluate()
    assert isinstance(i, String)
    assert i.value == "test"


def test_serde() -> None:
    """String can be converted to model and back."""
    i = String("test").with_metadata(get_sample_evidence_metadata())

    model = i.to_model()
    e = String.from_model(model)

    assert e == i


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
) -> None:
    """String can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    i = String("test").with_metadata(get_sample_evidence_metadata())
    i.save_with(ctx, store)

    loaded = String.load_with("evidence.test_id", context=ctx, store=store)
    assert loaded == i


def test_equal_to() -> None:
    m = get_sample_evidence_metadata()

    validator = String.equal_to("test")

    res = validator.validate(String("test").with_metadata(m))
    assert bool(res)

    res = validator.validate(String("no test").with_metadata(m))
    assert not bool(res)


def test_contains() -> None:
    m = get_sample_evidence_metadata()

    validator = String.contains("test")

    res = validator.validate(String("test").with_metadata(m))
    assert bool(res)

    res = validator.validate(String("This is a test.").with_metadata(m))
    assert bool(res)

    res = validator.validate(String("Other random sentence.").with_metadata(m))
    assert not bool(res)
