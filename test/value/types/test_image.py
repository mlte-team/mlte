"""
test/value/types/test_image.py

Unit tests for Image.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.store.artifact.store import ArtifactStore
from mlte.value.types.image import Image
from test.store.artifact.fixture import store_with_context  # noqa


def get_sample_image_path() -> Path:
    return Path("test/value/types/flower3.jpg")


def test_from_str():
    """Image can be loaded from filesystem path as string."""

    local_path = str(get_sample_image_path())
    _ = Image(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        local_path,
    )


def test_from_path():
    """Image can be loaded from filesystem path as Path."""

    local_path = get_sample_image_path()
    _ = Image(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        local_path,
    )


def test_from_bytes():
    """Image can be loaded from bytes."""

    local_path = get_sample_image_path()

    with local_path.open("rb") as f:
        image = f.read()
    _ = Image(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        image,
    )


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Image can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    local_path = get_sample_image_path()

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Image(m, local_path)
    i.save_with(ctx, store)

    # NOTE(Kyle): No equality test implemented.
    _ = Image.load_with("id.value", context=ctx, store=store)


def test_ignore() -> None:
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )

    local_path = str(get_sample_image_path())

    msg = "Just writing some data"
    cond = Image.ignore(msg)

    res = cond(Image(m, local_path))
    assert res.message == msg
