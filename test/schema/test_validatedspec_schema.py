"""
test/schema/test_validatedspec_schema.py

Unit tests for ValidatedSpec schema.
"""


import mlte
from mlte.spec import Spec, Requirement, SpecValidator
from mlte.property.costs import StorageCost
from mlte.value.types import Integer
from mlte.evidence import EvidenceMetadata
from mlte.api import read_validatedspec
from mlte._private.schema import validate_validatedspec_schema


def test_schema(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    spec = Spec(
        {StorageCost("rationale"): [Requirement("id", Integer.less_than(3))]}
    )
    specValidator = SpecValidator(spec)
    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value(i)
    validatedSpec = specValidator.validate()
    validatedSpec.save()

    doc = read_validatedspec(f"local://{tmp_path}", "model", "0.0.1")
    validate_validatedspec_schema(doc)
