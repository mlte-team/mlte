"""
test/schema/test_spec_schema.py

Unit tests for Spec schema.
"""


from mlte._private.schema import validate_spec_schema
from mlte.property.costs import StorageCost
from mlte.spec.spec import Spec
from mlte.value.types.integer import Integer

from ..fixture.store import store_with_context  # noqa


def test_instance_with_content():
    spec = Spec(
        properties={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )

    doc = spec.to_model().to_json()
    validate_spec_schema(doc["body"])
