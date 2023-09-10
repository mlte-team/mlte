"""
test/schema/test_spec_schema.py

Unit tests for Spec schema.
"""

from mlte.property.costs import StorageCost
from mlte.spec.spec import Spec
from mlte.value.types.integer import Integer

from . import util as util


def test_instance_with_content():
    spec = Spec(
        properties={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )

    doc = spec.to_model().to_json()
    util.validate_spec_schema(doc["body"])
