"""
Unit tests for ValidatedSpec functionality.
"""
from __future__ import annotations

import pytest

import mlte
from mlte.spec import Spec, ValidatedSpec, Requirement, SpecValidator
from mlte.property.costs import StorageCost
from mlte.value.types import Integer
from mlte.evidence import EvidenceMetadata
from mlte.validation import Result
from mlte.measurement.storage import LocalObjectSize


def test_save_load(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    spec = Spec(
        {StorageCost("rationale"): [Requirement("id", Integer.less_than(3))]}
    )
    specValidator = SpecValidator(spec)

    # A dummy result
    i = Integer(EvidenceMetadata("typename", "id"), 1)
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    validatedSpec.save()

    r = ValidatedSpec.load()
    assert r == validatedSpec


def test_no_result():
    # Spec does not have value for requirement.
    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement("test", LocalObjectSize.value().less_than(3))
            ]
        }
    )

    results: dict[str, Result] = {}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec.generate_validatedspec(spec, results)
