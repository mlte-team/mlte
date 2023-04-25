"""
Unit tests for BoundSpec functionality.
"""

import mlte
from mlte.spec import Spec, BoundSpec, Condition, SpecValidator
from mlte.property.costs import StorageCost
from mlte.value.types import Integer
from mlte.measurement_metadata import MeasurementMetadata
from mlte.measurement import ExternalMeasurement

def test_save_load(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    spec = Spec({StorageCost("rationale"): [Condition("test", ExternalMeasurement.__name__, "less_than", 3)]})
    specValidator = SpecValidator(spec)

    # A dummy result
    i = Integer(MeasurementMetadata("typename", "id"), 1)
    specValidator.add_value("StorageCost", "test", i)
    
    bound = specValidator.validate()
    bound.save()

    r = BoundSpec.load()
    assert r == bound
