"""
test/artifact/test_artifact.py

Unit tests for MLTE artifact protocol implementation.
"""

from typing import Tuple

import pytest

from mlte.artifact.artifact import Artifact
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.evidence.types.real import Real
from mlte.negotiation.artifact import NegotiationCard
from mlte.report.artifact import Report
from mlte.results.test_results import TestResults
from mlte.session.session import set_context, set_store
from mlte.store.artifact.store import ArtifactStore
from mlte.store.base import StoreType, StoreURI
from mlte.tests.test_suite import TestSuite
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa
from test.store.artifact.fixture import FX_MODEL_ID, FX_VERSION_ID


def test_save_load_session() -> None:
    """
    Artifacts can be saved  and loaded from global session.

    TODO(Kyle): Can we make this parametric over artifact types?
    """

    set_context(FX_MODEL_ID, FX_VERSION_ID)
    set_store(f"{StoreURI.get_default_prefix(StoreType.LOCAL_MEMORY)}")

    a = NegotiationCard("my-card")

    a.save(parents=True)
    _ = NegotiationCard.load("my-card")


def fill_test_store(ctx: Context, store: ArtifactStore):
    """Fills a sample store."""
    n1 = NegotiationCard("test-card")
    n2 = NegotiationCard("test-card2")
    s1 = TestSuite(identifier="test-spec1")
    s2 = TestSuite(identifier="test-spec2")
    vs1 = TestResults(identifier="test-validated1", test_suite=s1)
    vs2 = TestResults(identifier="test-validated2", test_suite=s2)
    m1 = get_sample_evidence_metadata(test_case_id="id1")
    v1 = Integer(10).with_metadata(m1)
    m2 = get_sample_evidence_metadata(test_case_id="id2")
    v2 = Real(3.14).with_metadata(m2)
    r1 = Report("r1")
    r2 = Report("r2")

    n1.save_with(ctx, store, parents=True)
    n2.save_with(ctx, store)
    s1.save_with(ctx, store)
    s2.save_with(ctx, store)
    vs1.save_with(ctx, store)
    vs2.save_with(ctx, store)
    v1.save_with(ctx, store)
    v2.save_with(ctx, store)
    r1.save_with(ctx, store)
    r2.save_with(ctx, store)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_load_all_models(
    artifact_type: ArtifactType,
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
):
    """
    Loading all models of a given type.
    """
    store, ctx = store_with_context
    fill_test_store(ctx, store)

    models = Artifact.load_models(artifact_type, ctx, store)

    assert len(models) == 2
    assert models[0].header.type == artifact_type
