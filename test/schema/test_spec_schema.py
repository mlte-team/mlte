"""
test/schema/test_spec_schema.py

Unit tests for Spec schema.
"""

import pytest

from mlte._private.schema import validate_spec_schema
from mlte.api import read_spec
from mlte.property.costs import StorageCost
from mlte.spec import Requirement, Spec
from mlte.value.types import Integer


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_instance_with_content(tmp_path):
    spec = Spec(
        {StorageCost("test"): [Requirement("test", Integer.less_than(3))]}
    )
    spec.save()

    doc = read_spec(f"local://{tmp_path}", "model", "0.0.1")
    validate_spec_schema(doc)
