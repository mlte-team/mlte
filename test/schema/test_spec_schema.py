"""
Unit tests for Spec schema.
"""

import mlte
from mlte.spec import Spec
from mlte.property.costs import StorageCost
from mlte._private.schema import validate_spec_schema
from mlte.store.api import read_spec


def test_instance_with_content(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    spec = Spec(StorageCost())
    spec.save()

    doc = read_spec(f"local://{tmp_path}", "model", "0.0.1")
    validate_spec_schema(doc)
