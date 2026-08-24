"""Unit tests for Unavailable."""

from __future__ import annotations

from mlte.context.context import Context
from mlte.evidence.artifact import Evidence
from mlte.evidence.types.string import String
from mlte.evidence.types.unavailable import Unavailable
from mlte.measurement.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from test.evidence.types.helper import get_sample_evidence_metadata


class BrokenMeasurement(Measurement):
    def __call__(self, first_arg: str, *args, **kwargs) -> Evidence:
        raise Exception("ERRROR!!!")

    @classmethod
    def output(cls) -> type[Evidence]:
        return String


def test_serde() -> None:
    """Unavailable can be converted to model and back."""
    i = Unavailable(details="test", traceback="tb").with_metadata(
        get_sample_evidence_metadata()
    )

    model = i.to_model()
    e = Unavailable.from_model(model)

    assert e == i


def test_save_load(
    artifact_store_with_context: tuple[ArtifactStore, Context],
) -> None:
    """Unavailable can be saved to and loaded from artifact store."""
    store, ctx = artifact_store_with_context

    i = Unavailable(details="test", traceback="tb").with_metadata(
        get_sample_evidence_metadata()
    )
    i.save_with(ctx, store)

    loaded = Unavailable.load_with("evidence.test_id", context=ctx, store=store)
    assert loaded == i
