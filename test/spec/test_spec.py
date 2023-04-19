"""
Unit tests for Binding functionality.
"""

# TODO: re-write next text to be useful with new Spec usage.

"""
import pytest

import mlte
from mlte.spec import Spec
from mlte.property.costs import StorageCost

from mlte.value.types import Integer
from mlte.measurement.measurement_metadata import MeasurementMetadata


def test_save(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    s = Spec(StorageCost())
    s.save()

    r = Spec.load()
    assert s == r


def test_load_failure(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    with pytest.raises(RuntimeError):
        _ = Spec.load()

def test_compatibility0():
    # Binding does not cover spec; missing key

    s = Spec(StorageCost())
    b = Binding({"foobar": ["baz"]})

    i = Integer(MeasurementMetadata("dummy", "id"), 1)

    with pytest.raises(RuntimeError):
        _ = b.bind(s, [i])  # type: ignore


def test_compatibility1():
    # Binding does not cover spec; empty mapping

    s = Spec(StorageCost())
    b = Binding({"StorageCost": []})

    i = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)

    with pytest.raises(RuntimeError):
        _ = b.bind(s, [i])  # type: ignore


def test_compatibility2():
    # Binding includes extra property

    s = Spec(StorageCost())
    b = Binding({"StorageCost": ["id"], "foobar": ["baz"]})

    i = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)

    with pytest.raises(RuntimeError):
        _ = b.bind(s, [i])  # type: ignore


def test_bind_unique():
    # Collect with duplicated results should fail
    spec = Spec(StorageCost())
    i0 = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)
    i1 = Integer(MeasurementMetadata("dummy", Identifier("id")), 2)
    binding = Binding({"property": ["id"]})
    with pytest.raises(RuntimeError):
        _ = binding.bind(spec, [i0.less_than(3), i1.less_than(3)])


def test_bind_coverage():
    s = Spec(StorageCost())
    b = Binding({"StorageCost": ["id"]})
    with pytest.raises(RuntimeError):
        _ = b.bind(s, [])


def test_bind_extra0():
    # With strict = True, binding unnecessary result fails
    s = Spec(StorageCost())
    b = Binding({"StorageCost": ["i0"]})
    i0 = Integer(MeasurementMetadata("dummy", Identifier("i0")), 1)
    i1 = Integer(MeasurementMetadata("dummy", Identifier("i1")), 2)
    with pytest.raises(RuntimeError):
        _ = b.bind(s, [i0.less_than(3), i1.less_than(3)])


def test_success():
    s = Spec(StorageCost())
    b = Binding({"StorageCost": ["i0", "i1"]})
    i0 = Integer(MeasurementMetadata("dummy", Identifier("i0")), 1)
    i1 = Integer(MeasurementMetadata("dummy", Identifier("i1")), 2)

    _ = b.bind(s, [i0.less_than(3), i1.less_than(3)])
 """
