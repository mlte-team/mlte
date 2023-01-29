"""
Unit tests for Binding schema validation.
"""

import mlte
from mlte.binding import Binding
from mlte._private.schema import validate_binding_schema
from mlte.store.api import read_binding


def test_schema_validation(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    b = Binding({"property_name": ["id0", "id1"]})
    b.save()

    d = read_binding(f"local://{tmp_path}", "model", "0.0.1")
    validate_binding_schema(d)
