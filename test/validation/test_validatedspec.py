"""
test/validation/test_validatedspec.py

Unit tests for ValidatedSpec functionality.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.spec.spec import Spec
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.result import Result
from mlte.validation.spec_validator import SpecValidator
from mlte.validation.validated_spec import ValidatedSpec
from mlte.value.types.integer import Integer
from test.store.artifact.fixture import store_with_context  # noqa


def test_save_load(store_with_context: Tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context

    spec = Spec(
        qa_categories={StorageCost("rationale"): {"id": Integer.less_than(3)}}
    )
    specValidator = SpecValidator(spec)

    # A dummy value
    i = Integer(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        1,
    )
    specValidator.add_value(i)

    validatedSpec = specValidator.validate()
    validatedSpec.save_with(ctx, store)

    r = ValidatedSpec.load_with(context=ctx, store=store)
    assert r == validatedSpec


def test_no_result_and_no_qa_category():
    # Spec does not have Result for condition, not even a qa category.
    spec = Spec(
        qa_categories={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )

    results: Dict[str, Dict[str, Result]] = {}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec(spec=spec, results=results)


def test_no_result():
    # Spec does not have Result for condition.
    spec = Spec(
        qa_categories={StorageCost("rationale"): {"test": Integer.less_than(3)}}
    )

    results: Dict[str, Dict[str, Result]] = {"StorageCost": {}}
    with pytest.raises(RuntimeError):
        _ = ValidatedSpec(spec=spec, results=results)
