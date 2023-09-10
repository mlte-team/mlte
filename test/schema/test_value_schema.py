"""
test/schema/test_value_schema.py

Unit tests for Value schema.
"""

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.value.types.integer import Integer
from mlte.value.types.opaque import Opaque
from mlte.value.types.real import Real

from . import util as util


def test_real():
    r = Real(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        3.14,
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_integer():
    r = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        3,
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])


def test_opaque():
    r = Opaque(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        {"foo": "bar"},
    )

    doc = r.to_model().to_json()
    util.validate_value_schema(doc["body"])
