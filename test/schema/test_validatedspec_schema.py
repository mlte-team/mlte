"""
test/schema/test_validatedspec_schema.py

Unit tests for ValidatedSpec schema.
"""

from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.types.integer import Integer
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import TestSuiteValidator

from . import util as util


def test_schema():
    spec = Spec(
        qa_categories={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = TestSuiteValidator(spec)
    i = Integer(
        EvidenceMetadata(measurement_class="typename", test_case_id="test"),
        1,
    )
    specValidator.add_value(i)
    validatedSpec = specValidator.validate()

    doc = validatedSpec.to_model().to_json()
    util.validate_validatedspec_schema(doc["body"])
