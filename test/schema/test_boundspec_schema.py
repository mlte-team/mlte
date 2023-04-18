"""
Unit tests for BoundSpec schema.
"""

# TODO: Update tests

"""

import mlte
from mlte.spec import Spec
from mlte.property.costs import StorageCost
from mlte.value import Integer
from mlte.measurement.measurement_metadata import MeasurementMetadata
from mlte.measurement.identifier import Identifier
from mlte.store.api import read_boundspec
from mlte._private.schema import validate_boundspec_schema

def test_schema(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    # A dummy result
    i = Integer(MeasurementMetadata("typename", Identifier("id")), 1)

    spec = Spec(StorageCost())
    binding = Binding({"StorageCost": ["id"]})
    bound = binding.bind(spec, [i.less_than(3)])
    bound.save()

    doc = read_boundspec(f"local://{tmp_path}", "model", "0.0.1")
    validate_boundspec_schema(doc)
 """
