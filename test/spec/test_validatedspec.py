"""
test/spec/test_validatedspec.py

Unit tests for ValidatedSpec functionality.
"""

from __future__ import annotations

from typing import Dict

import pytest

from mlte.evidence.identifier import Identifier
from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.storage import LocalObjectSize
from mlte.property.costs import StorageCost
from mlte.spec import Requirement, Spec, SpecValidator, ValidatedSpec
from mlte.validation import Result
from mlte.value.types.integer import Integer


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_save_load(tmp_path):
    spec = Spec(
        {StorageCost("rationale"): [Requirement("id", Integer.less_than(3))]}
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
        {
            StorageCost("rationale"): [
                Requirement("test", LocalObjectSize.value().less_than(3))
            ]
        }
    )

    results: Dict[str, Result] = {}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec(spec, results)
