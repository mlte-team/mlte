"""
Unit tests for TestResults functionality.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.results.result import Failure, Info, Result
from mlte.results.test_results import TestResults
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.test_suite import TestSuite
from mlte.validation.test_suite_validator import TestSuiteValidator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.fixture.artifact import ArtifactModelFactory
from test.store.artifact.fixture import store_with_context  # noqa


def test_save_load(store_with_context: Tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context

    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE, complete=True)
    )
    test_suite_validator = TestSuiteValidator(test_suite)

    # A dummy value
    i = Integer(1).with_metadata(
        get_sample_evidence_metadata(test_case_id="Test1")
    )
    test_suite_validator.add_evidence(i)

    test_results = test_suite_validator.validate()
    test_results.save_with(ctx, store)

    r = TestResults.load_with(context=ctx, store=store)
    assert r == test_results


def test_no_result():
    # TestSuite does not have Result for evidence.
    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE, complete=True)
    )

    results: Dict[str, Result] = {}
    with pytest.raises(RuntimeError):
        _ = TestResults(test_suite=test_suite, results=results)


def test_convert_results():
    # Results can be converted.

    test_id = "Test2"
    auto_msg = "please check manually"
    manual_msg = "I vouch for this"

    test_results = TestResults.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_RESULTS, complete=True)
    )
    test_results.results[test_id] = Info(manual_msg)

    test_results.convert_result(test_id, Failure, auto_msg)

    result = test_results.results[test_id]
    assert type(result) is Failure
    assert (
        result.message
        == f"Manually validated: {auto_msg} (original message: {manual_msg})"
    )
