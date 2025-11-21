"""Unit tests for Value."""

from typing import Tuple

from mlte.context.context import Context
from mlte.evidence.artifact import Evidence
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.types.integer import Integer
from mlte.evidence.types.real import Real
from mlte.measurement.model import MeasurementMetadata
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa


def test_load_all(
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
):
    """
    Loading all models of a given type.
    """
    store, ctx = store_with_context

    m1 = EvidenceMetadata(
        measurement=MeasurementMetadata(
            measurement_class="typename", output_class="output"
        ),
        test_case_id="id1",
    )
    v1 = Integer(10).with_metadata(m1)
    m2 = EvidenceMetadata(
        measurement=MeasurementMetadata(
            measurement_class="typename", output_class="output"
        ),
        test_case_id="id2",
    )
    v2 = Real(3.14).with_metadata(m2)
    v1.save_with(ctx, store, parents=True)
    v2.save_with(ctx, store)

    models = Evidence.load_all_with(ctx, store)

    assert len(models) == 2
    assert models[0] == v1 or models[0] == v2
    assert models[1] == v1 or models[1] == v2
