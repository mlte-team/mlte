"""
Unit tests for Spec functionality.
"""

import pytest

import mlte
from mlte.spec import Spec
from mlte.binding import Binding
from mlte.property.costs import StorageCost
from mlte.measurement.result import Integer
from mlte.measurement.measurement_metadata import MeasurementMetadata
from mlte.measurement.identifier import Identifier


def test_save(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    s = Spec({StorageCost(): []})
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

    s = Spec({StorageCost(): []})
    b = Binding({"foobar": ["baz"]})

    i = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)

    with pytest.raises(RuntimeError):
        _ = s.bind(b, [i])  # type: ignore


def test_compatibility1():
    # Binding does not cover spec; empty mapping

    s = Spec({StorageCost(): []})
    b = Binding({"StorageCost": []})

    i = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)

    with pytest.raises(RuntimeError):
        _ = s.bind(b, [i])  # type: ignore


def test_compatibility2():
    # Binding includes extra property

    s = Spec({StorageCost(): []})
    b = Binding({"StorageCost": ["id"], "foobar": ["baz"]})

    i = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)

    with pytest.raises(RuntimeError):
        _ = s.bind(b, [i])  # type: ignore


def test_bind_unique():
    # Collect with duplicated results should fail
    spec = Spec({StorageCost(): []})
    i0 = Integer(MeasurementMetadata("dummy", Identifier("id")), 1)
    i1 = Integer(MeasurementMetadata("dummy", Identifier("id")), 2)
    with pytest.raises(RuntimeError):
        _ = spec.bind(
            Binding({"property": ["id"]}), [i0.less_than(3), i1.less_than(3)]
        )


def test_bind_coverage():
    s = Spec({StorageCost(): []})
    b = Binding({"StorageCost": ["id"]})
    with pytest.raises(RuntimeError):
        _ = s.bind(b, [])


def test_bind_extra0():
    # With strict = True, binding unnecessary result fails
    s = Spec({StorageCost(): []})
    b = Binding({"StorageCost": ["i0"]})
    i0 = Integer(MeasurementMetadata("dummy", Identifier("i0")), 1)
    i1 = Integer(MeasurementMetadata("dummy", Identifier("i1")), 2)
    with pytest.raises(RuntimeError):
        _ = s.bind(b, [i0.less_than(3), i1.less_than(3)])


def test_success():
    s = Spec({StorageCost(): []})
    b = Binding({"StorageCost": ["i0", "i1"]})
    i0 = Integer(MeasurementMetadata("dummy", Identifier("i0")), 1)
    i1 = Integer(MeasurementMetadata("dummy", Identifier("i1")), 2)

    _ = s.bind(b, [i0.less_than(3), i1.less_than(3)])
