"""
test/value/types/test_image.py

Unit tests for Image.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from mlte.context.context import Context
from mlte.evidence.types.image import Image
from mlte.store.artifact.store import ArtifactStore
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa


def get_sample_image_path() -> Path:
    return Path("test/evidence/types/flower3.jpg")


def test_from_str():
    """Image can be loaded from filesystem path as string."""

    local_path = str(get_sample_image_path())
    _ = Image(local_path).with_metadata(get_sample_evidence_metadata())


def test_from_path():
    """Image can be loaded from filesystem path as Path."""

    local_path = get_sample_image_path()
    _ = Image(local_path).with_metadata(get_sample_evidence_metadata())


def test_from_bytes():
    """Image can be loaded from bytes."""

    local_path = get_sample_image_path()

    with local_path.open("rb") as f:
        image = f.read()
    _ = Image(image).with_metadata(get_sample_evidence_metadata())


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
) -> None:
    """Image can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    local_path = get_sample_image_path()

    i = Image(local_path).with_metadata(get_sample_evidence_metadata())
    i.save_with(ctx, store)

    # NOTE(Kyle): No equality test implemented.
    _ = Image.load_with("evidence.test_id", context=ctx, store=store)


def test_ignore() -> None:
    local_path = str(get_sample_image_path())

    msg = "Just writing some data"
    validator = Image.register_info(msg)

    res = validator.validate(
        Image(local_path).with_metadata(get_sample_evidence_metadata())
    )
    assert res.message == msg
