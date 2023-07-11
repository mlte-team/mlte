"""
Unit tests for Value schema.
"""

import mlte
from mlte._private.schema import validate_value_schema
from mlte.api import read_value
from mlte.evidence.evidence_metadata import EvidenceMetadata
from mlte.value.types import Integer, Opaque, Real


def test_real(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Real(EvidenceMetadata("typename", "id"), 3.14)
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)


def test_integer(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Integer(EvidenceMetadata("typename", "id"), 3)
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)


def test_opaque(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    r = Opaque(EvidenceMetadata("typename", "id"), {"foo": "bar"})
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)
