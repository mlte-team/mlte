"""
test/schema/test_validatedspec_schema.py

Unit tests for ValidatedSpec schema.
"""

import pytest

from mlte._private.schema import validate_validatedspec_schema
from mlte.api import read_validatedspec
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.property.costs import StorageCost
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import SpecValidator
from mlte.value.types.integer import Integer


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_schema(tmp_path):
    spec = Spec(
        "spec", {StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)
    i = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        1,
    )
    specValidator.add_value(i)
    validatedSpec = specValidator.validate()
    validatedSpec.save()

    doc = read_validatedspec(f"local://{tmp_path}", "model", "0.0.1")
    validate_validatedspec_schema(doc)
