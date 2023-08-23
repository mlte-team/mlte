"""
test/spec/test_validatedspec.py

Unit tests for ValidatedSpec functionality.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.property.costs import StorageCost
from mlte.spec.spec import Spec
from mlte.store.base import Store
from mlte.validation.result import Result
from mlte.validation.spec_validator import SpecValidator
from mlte.validation.validated_spec import ValidatedSpec
from mlte.value.types.integer import Integer

from ..fixture.store import store_with_context  # noqa


def test_save_load(store_with_context: Tuple[Store, Context]):  # noqa
    store, ctx = store_with_context

    spec = Spec({StorageCost("rationale"): {"id": Integer.less_than(3)}})
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
    validatedSpec.save_with(ctx, store)

    r = ValidatedSpec.load_with("spec.validated", ctx, store)
    assert r == validatedSpec


def test_no_result_and_no_property():
    # Spec does not have Result for condition, not even a property.
    spec = Spec({StorageCost("rationale"): {"test": Integer.less_than(3)}})

    results: Dict[str, Dict[str, Result]] = {}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec(spec, results)


def test_no_result():
    # Spec does not have Result for condition.
    spec = Spec({StorageCost("rationale"): {"test": Integer.less_than(3)}})

    results: Dict[str, Dict[str, Result]] = {"StorageCost": {}}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec(spec, results)
