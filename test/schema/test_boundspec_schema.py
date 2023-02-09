"""
Unit tests for BoundSpec schema.
"""

import mlte
from mlte.spec import Spec
from mlte.binding import Binding
from mlte.property.costs import StorageCost
from mlte.measurement.result import Integer
from mlte.measurement import MeasurementMetadata, Identifier
from mlte.store.api import read_boundspec
from mlte._private.schema import validate_boundspec_schema


def test_schema(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    # A dummy result
    i = Integer(MeasurementMetadata("typename", Identifier("id")), 1)

    spec = Spec(StorageCost())
    bound = spec.bind(Binding({"StorageCost": ["id"]}), [i.less_than(3)])
    bound.save()

    doc = read_boundspec(f"local://{tmp_path}", "model", "0.0.1")
    validate_boundspec_schema(doc)
