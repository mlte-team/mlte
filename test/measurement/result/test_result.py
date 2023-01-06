"""
Unit tests for generic Results.
"""

from __future__ import annotations

import pytest
from typing import Dict, Any

import mlte
from mlte.property.costs import StorageCost
from mlte.measurement import MeasurementMetadata
from mlte.measurement.result import Result


class DummyResult(Result):
    def __init__(self, measurement_metadata: MeasurementMetadata):
        super().__init__(self, measurement_metadata)

    def serialize(self) -> Dict[str, Any]:
        return {}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> DummyResult:
        return DummyResult(measurement_metadata)


def test_bind():
    p = StorageCost()
    m = MeasurementMetadata("typename", "identifier")
    r = DummyResult(m)

    r.bind(p)

    assert r.binding.is_bound()
    assert r.binding.is_bound_to(p)


def test_bind_persists_across_serde(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    p = StorageCost()
    m = MeasurementMetadata("typename", "identifier")
    r = DummyResult(m)

    r.bind(p)
    r.save()

    r = DummyResult.load("identifier")

    assert r.binding.is_bound()
    assert r.binding.is_bound_to(p)


def test_rebind_failure():
    p = StorageCost()
    m = MeasurementMetadata("typename", "identifier")
    r = DummyResult(m)

    r.bind(p)

    with pytest.raises(RuntimeError):
        r.bind(p)
