"""
Unit tests for generic Results.
"""

from __future__ import annotations

import pytest
from typing import Dict, Any

from mlte.property.costs import StorageCost
from mlte.measurement import MeasurementMetadata
from mlte.measurement.result import Result
from mlte.measurement.validation import Validator, Success


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

    v = Validator("validator", lambda r: Success())(r)
    v.bind(p)

    assert v.result.binding.is_bound()
    assert v.result.binding.is_bound_to(p)


def test_rebind_failure():
    p = StorageCost()
    m = MeasurementMetadata("typename", "identifier")
    r = DummyResult(m)

    v = Validator("validator", lambda r: Success())(r)
    v.bind(p)

    with pytest.raises(RuntimeError):
        v.bind(p)
