"""
test/value/types/test_image.py

Unit tests for Image.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import requests

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.store.artifact.store import ArtifactStore
from mlte.value.types.image import Image
from test.store.artifact.fixture import store_with_context  # noqa

# A cute image for testing purposes
IMAGE_URL = "https://images.unsplash.com/photo-1615497001839-b0a0eac3274c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8Y3V0ZSUyMGNhdHxlbnwwfHwwfHw%3D&w=1000&q=80"  # noqa


def download_image(dst_dir: Path) -> Path:
    """Download image and return complete path."""
    dst_path = dst_dir / "image"
    r = requests.get(IMAGE_URL)
    with dst_path.open("wb") as f:
        f.write(r.content)
    return dst_path


def test_from_str(tmp_path):
    """Image can be loaded from filesystem path as string."""

    local_path = str(download_image(tmp_path))
    _ = Image(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        local_path,
    )


def test_from_path(tmp_path):
    """Image can be loaded from filesystem path as Path."""

    local_path = download_image(tmp_path)
    _ = Image(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        local_path,
    )


def test_from_bytes(tmp_path):
    """Image can be loaded from bytes."""

    local_path = download_image(tmp_path)

    with local_path.open("rb") as f:
        image = f.read()
    _ = Image(
        EvidenceMetadata(
            measurement_type="typename", identifier=Identifier(name="id")
        ),
        image,
    )


def test_save_load(
    tmp_path, store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Image can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    local_path = download_image(tmp_path)

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Image(m, local_path)
    i.save_with(ctx, store)

    # NOTE(Kyle): No equality test implemented.
    _ = Image.load_with("id.value", context=ctx, store=store)
