"""
test/schema/test_value_schema.py

Unit tests for Value schema.
"""

import pytest

from mlte._private.schema import validate_value_schema
from mlte.api import read_value
from mlte.evidence.evidence_metadata import EvidenceMetadata
from mlte.value.types import Integer, Opaque, Real


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_real(tmp_path):
    r = Real(EvidenceMetadata("typename", "id"), 3.14)
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_integer(tmp_path):
    r = Integer(EvidenceMetadata("typename", "id"), 3)
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_opaque(tmp_path):
    r = Opaque(EvidenceMetadata("typename", "id"), {"foo": "bar"})
    r.save()

    d = read_value(f"local://{tmp_path}", "model", "0.0.1", "id")
    validate_value_schema(d)
