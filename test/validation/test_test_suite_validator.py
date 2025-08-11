"""
Unit tests for TestSuiteValidator functionality.
"""

from __future__ import annotations

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.session.session import session, set_context
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.test_suite import TestSuite
from mlte.validation.test_suite_validator import TestSuiteValidator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.fixture.artifact import ArtifactModelFactory


def test_no_requirement():
    # Test Sute Validator does not have value for evidence.
    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE, complete=True)
    )
    test_suite_validator = TestSuiteValidator(test_suite)

    i = Integer(1).with_metadata(get_sample_evidence_metadata())
    test_suite_validator.add_evidence(i)

    with pytest.raises(RuntimeError):
        _ = test_suite_validator.validate()


def test_success():
    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE, complete=True)
    )
    test_suite_validator = TestSuiteValidator(test_suite)

    m = get_sample_evidence_metadata(test_case_id="Test1")

    i = Integer(1).with_metadata(m)
    test_suite_validator.add_evidence(i)

    test_results = test_suite_validator.validate()
    assert test_results is not None


def test_success_defaults(store_with_context: tuple[ArtifactStore, Context]):
    """Tests that validator can load default TestSuite and all Evidence from current session, and validate it."""
    store, ctx = store_with_context
    set_context(model_id=ctx.model, version_id=ctx.version)
    session()._set_artifact_store(store)

    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE, complete=True)
    )
    test_suite.identifier = TestSuite.get_default_id()
    test_suite.save_with(ctx, store, parents=True)

    m = get_sample_evidence_metadata(test_case_id="Test1")
    i = Integer(1).with_metadata(m)
    i.save_with(ctx, store)

    test_suite_validator = TestSuiteValidator()
    test_results = test_suite_validator.load_and_validate()

    assert test_results is not None
    assert test_results.test_suite == test_suite
    assert len(test_results.results) == 1
