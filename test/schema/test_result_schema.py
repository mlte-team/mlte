"""
Unit tests for Result schema.
"""

import mlte
from mlte.measurement.result import Integer, Real, Opaque
from mlte.measurement import MeasurementMetadata, Identifier
from mlte._private.schema import validate_result_schema
from mlte.store.api import read_result


def test_real(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Real(MeasurementMetadata("typename", Identifier("id")), 3.14)
    r.save()

    d = read_result(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_result_schema(d)


def test_integer(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Integer(MeasurementMetadata("typename", Identifier("id")), 3)
    r.save()

    d = read_result(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_result_schema(d)


def test_opaque(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Opaque(
        MeasurementMetadata("typename", Identifier("id")), {"foo": "bar"}
    )
    r.save()

    d = read_result(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_result_schema(d)
