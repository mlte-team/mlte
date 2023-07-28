"""
test/schema/test_validatedspec_schema.py

Unit tests for ValidatedSpec schema.
"""

import pytest

from mlte._private.schema import validate_validatedspec_schema
from mlte.api import read_validatedspec
from mlte.evidence import EvidenceMetadata
from mlte.property.costs import StorageCost
from mlte.spec import Requirement, Spec, SpecValidator
from mlte.value.types import Integer


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_schema(tmp_path):
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
