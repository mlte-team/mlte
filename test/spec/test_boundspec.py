"""
Unit tests for BoundSpec functionality.
"""

# TODO: update tests

"""

import mlte
from mlte.spec import Spec, BoundSpec
from mlte.property.costs import StorageCost
from mlte.value import Integer
from mlte.measurement.measurement_metadata import MeasurementMetadata

def test_save_load(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    # A dummy result
    i = Integer(MeasurementMetadata("typename", "id"), 1)

    spec = Spec(StorageCost())
    binding = Binding({"StorageCost": ["id"]})
    bound = binding.bind(spec, [i.less_than(3)])
    bound.save()

    r = BoundSpec.load()
    assert r == bound
 """
