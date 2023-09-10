"""
test/schema/test_validatedspec_schema.py

Unit tests for ValidatedSpec schema.
"""


from mlte._private.schema import validate_validatedspec_schema
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.property.costs import StorageCost
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import SpecValidator
from mlte.value.types.integer import Integer


def test_schema():
    spec = Spec(
        properties={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)
    i = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="test")
        ),
        1,
    )
    specValidator.add_value(i)
    validatedSpec = specValidator.validate()

    doc = validatedSpec.to_model().to_json()
    validate_validatedspec_schema(doc["body"])
