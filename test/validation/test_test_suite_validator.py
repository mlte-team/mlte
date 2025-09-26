"""
Unit tests for TestSuiteValidator functionality.
"""

from __future__ import annotations

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.evidence.types.real import Real
from mlte.measurement.storage.local_object_size import LocalObjectSize
from mlte.session.session import session, set_context
from mlte.session.session_stores import SessionStores
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.test_case import TestCase
from mlte.tests.test_suite import TestSuite
from mlte.validation.test_suite_validator import TestSuiteValidator
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.fixture.artifact import ArtifactModelFactory


def test_no_requirement():
    # Test Sute Validator does not have value for evidence.
    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE)
    )
    test_suite_validator = TestSuiteValidator(test_suite)

    i = Integer(1).with_metadata(get_sample_evidence_metadata())
    test_suite_validator.add_evidence(i)

    with pytest.raises(RuntimeError):
        _ = test_suite_validator.validate()


def test_success():
    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE)
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
    session()._stores = SessionStores()
    session().stores.set_artifact_store(store)

    test_suite = TestSuite.from_model(
        ArtifactModelFactory.make(ArtifactType.TEST_SUITE)
    )
    test_suite.identifier = TestSuite.build_full_id()
    test_suite.save_with(ctx, store, parents=True)

    m = get_sample_evidence_metadata(test_case_id="Test1")
    i = Integer(1).with_metadata(m)
    i.save_with(ctx, store)

    test_suite_validator = TestSuiteValidator()
    test_results = test_suite_validator.load_and_validate()

    assert test_results is not None
    assert test_results.test_suite == test_suite
    assert len(test_results.results) == 1


def test_suite_validate():
    """Test that we can validate with regular, info, and info+no evidence cases."""
    test_suite = TestSuite(
        test_cases=[
            TestCase(
                identifier="case1",
                goal="Check storage consumption",
                quality_scenarios=["qas1"],
                validator=LocalObjectSize.get_output_type().less_than(
                    150000000
                ),
                measurement=LocalObjectSize("model size"),
            ),
            TestCase(
                identifier="case2",
                goal="Check storage consumption",
                quality_scenarios=["qas2"],
                validator=Validator.build_info_validator(
                    "This will have evidence BUT has to be manually validated"
                ),
            ),
            TestCase(
                identifier="case3",
                goal="Check storage consumption",
                quality_scenarios=["qas3"],
                validator=Validator.build_info_validator(
                    "This will have no evidence and has to be manually validated"
                ),
            ),
        ]
    )

    test_suite_validator = TestSuiteValidator(test_suite)

    m = get_sample_evidence_metadata(test_case_id="case1")
    i = Real(1.0).with_metadata(m)
    test_suite_validator.add_evidence(i)

    m = get_sample_evidence_metadata(test_case_id="case2")
    i = Real(1.0).with_metadata(m)
    test_suite_validator.add_evidence(i)

    test_results = test_suite_validator.validate()

    assert test_results is not None
    assert len(test_results.results) == 3
    for case_id, result in test_results.results.items():
        if case_id == "case1":
            assert str(result) == "Success"
        else:
            assert str(result) == "Info"
