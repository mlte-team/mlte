"""
Unit tests for BoundSpec functionality.
"""

import mlte
from mlte.spec import Spec, BoundSpec
from mlte.binding import Binding
from mlte.property.costs import StorageCost
from mlte.measurement.result import Integer
from mlte.measurement.measurement_metadata import MeasurementMetadata
from mlte.measurement.identifier import Identifier


def test_save_load(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    # A dummy result
    i = Integer(MeasurementMetadata("typename", Identifier("id")), 1)

    spec = Spec(properties=[StorageCost()])
    bound = spec.bind(Binding({"StorageCost": ["id"]}), [i.less_than(3)])
    bound.save()

    r = BoundSpec.load()
    assert r == bound
