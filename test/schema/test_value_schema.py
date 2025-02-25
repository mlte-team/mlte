"""
test/schema/test_value_schema.py

Unit tests for Value schema.
"""

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.evidence.types.integer import Integer
from mlte.evidence.types.opaque import Opaque
from mlte.evidence.types.real import Real

from . import util as util


def test_real():
    r = Real(
        EvidenceMetadata(
            measurement_class="typename", test_case_id=Identifier(name="id")
        ),
        3.14,
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_integer():
    r = Integer(
        EvidenceMetadata(
            measurement_class="typename", test_case_id=Identifier(name="id")
        ),
        3,
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_opaque():
    r = Opaque(
        EvidenceMetadata(
            measurement_class="typename", test_case_id=Identifier(name="id")
        ),
        {"foo": "bar"},
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])
