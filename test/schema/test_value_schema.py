"""
test/schema/test_value_schema.py

Unit tests for Value schema.
"""

from mlte.evidence.types.integer import Integer
from mlte.evidence.types.opaque import Opaque
from mlte.evidence.types.real import Real
from test.evidence.types.helper import get_sample_evidence_metadata

from . import util as util


def test_real():
    r = Real(3.14)
    r.with_metadata(get_sample_evidence_metadata())

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_integer():
    r = Integer(3)
    r.with_metadata(get_sample_evidence_metadata())

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_opaque():
    r = Opaque(
        {"foo": "bar"},
    )
    r.with_metadata(get_sample_evidence_metadata())

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])
