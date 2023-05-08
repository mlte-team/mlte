"""
Unit tests for BoundSpec schema.
"""


import mlte
from mlte.spec import Spec, Condition, SpecValidator
from mlte.property.costs import StorageCost
from mlte.value.types import Integer
from mlte.evidence import EvidenceMetadata
from mlte.measurement import ExternalMeasurement
from mlte.api import read_boundspec
from mlte._private.schema import validate_boundspec_schema


def test_schema(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    spec = Spec(
        {
            StorageCost("rationale"): [
                Condition("test", ExternalMeasurement.__name__, "less_than", 3)
            ]
        }
    )
    specValidator = SpecValidator(spec)
    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value("StorageCost", "test", i)
    bound = specValidator.validate()
    bound.save()

    doc = read_boundspec(f"local://{tmp_path}", "model", "0.0.1")
    validate_boundspec_schema(doc)
