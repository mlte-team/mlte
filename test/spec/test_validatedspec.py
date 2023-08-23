"""
test/spec/test_validatedspec.py

Unit tests for ValidatedSpec functionality.
"""

from __future__ import annotations

from typing import Dict

import pytest

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.property.costs import StorageCost
from mlte.spec.spec import Spec
from mlte.spec.spec_validator import SpecValidator
from mlte.spec.validated_spec import ValidatedSpec
from mlte.validation.result import Result
from mlte.value.types.integer import Integer


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_save_load(tmp_path):
    spec = Spec(
        "spec", {StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)

    # A dummy result
    i = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        1,
    )
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    validatedSpec.save()

    r = ValidatedSpec.load()
    assert r == validatedSpec


def test_no_result():
    # Spec does not have Result for requirement.
    spec = Spec(
        "spec", {StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )

    results: Dict[str, Result] = {}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec(spec, results)
