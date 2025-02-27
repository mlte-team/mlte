"""
test/schema/test_value_schema.py

Unit tests for Value schema.
"""

from mlte.evidence.types.integer import Integer
from mlte.evidence.types.opaque import Opaque
from mlte.evidence.types.real import Real
from test.value.types.helper import get_sample_evidence_metadata

from . import util as util


def test_real():
    r = Real(
        get_sample_evidence_metadata(),
        3.14,
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_integer():
    r = Integer(
        get_sample_evidence_metadata(),
        3,
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_opaque():
    r = Opaque(
        get_sample_evidence_metadata(),
        {"foo": "bar"},
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])
