"""
Unit tests for ValidatedSpec functionality.
"""

import mlte
from mlte.spec import Spec, ValidatedSpec, Requirement, SpecValidator
from mlte.property.costs import StorageCost
from mlte.value.types import Integer
from mlte.evidence import EvidenceMetadata
from mlte.measurement import ExternalMeasurement


def test_save_load(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement("id", ExternalMeasurement.__name__, "less_than", 3)
            ]
        }
    )
    specValidator = SpecValidator(spec)

    # A dummy result
    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    validatedSpec.save()

    r = ValidatedSpec.load()
    assert r == validatedSpec
