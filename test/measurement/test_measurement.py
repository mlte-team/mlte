"""
Unit tests for generic Measurement.
"""

import pytest

from mlte.property.costs import StorageCost
from mlte.measurement import Measurement
from mlte.measurement.result import Integer


class DummyMeasurement(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Integer:
        return Integer(self.metadata, 1)


def test_bind():
    p = StorageCost()

    m = DummyMeasurement("identifier")
    m.bind(p)

    assert m.binding.is_bound()
    assert m.binding.is_bound_to(p)


def test_rebind_failure():
    p = StorageCost()

    m = DummyMeasurement("identifier")
    m.bind(p)

    # Attempting to bind again should fail
    with pytest.raises(RuntimeError):
        m.bind(p)
