"""
Unit tests for Value schema.
"""

import mlte
from mlte.value import Integer, Real, Opaque
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata
from mlte._private.schema import validate_value_schema
from mlte.store.api import read_value


def test_real(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Real(MeasurementMetadata("typename", "id"), 3.14)
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)


def test_integer(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Integer(MeasurementMetadata("typename", "id"), 3)
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)


def test_opaque(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Opaque(MeasurementMetadata("typename", "id"), {"foo": "bar"})
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)
