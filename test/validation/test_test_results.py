"""
test/validation/test_validatedspec.py

Unit tests for ValidatedSpec functionality.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.spec.test_suite import TestSuite
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.result import Result
from mlte.validation.test_results import TestResults
from mlte.validation.test_suite_validator import TestSuiteValidator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.fixture.artifact import ArtifactFactory
from test.store.artifact.fixture import store_with_context  # noqa


def test_save_load(store_with_context: Tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context

    test_suite = TestSuite.from_model(
        ArtifactFactory.make(ArtifactType.TEST_SUITE)
    )
    test_suite_validator = TestSuiteValidator(test_suite)

    # A dummy value
    i = Integer(1).with_metadata(
        get_sample_evidence_metadata(test_case_id="Test1")
    )
    test_suite_validator.add_evidence(i)

    validatedSpec = test_suite_validator.validate()
    validatedSpec.save_with(ctx, store)

    r = TestResults.load_with(context=ctx, store=store)
    assert r == validatedSpec


def test_no_result():
    # TestSuite does not have Result for evidence.
    test_suite = TestSuite.from_model(
        ArtifactFactory.make(ArtifactType.TEST_SUITE)
    )

    results: Dict[str, Result] = {}
    with pytest.raises(RuntimeError):
        _ = TestResults(test_suite=test_suite, results=results)
