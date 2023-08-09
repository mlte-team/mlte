"""
test/value/types/test_image.py

Unit tests for Image.
"""

from pathlib import Path

import pytest
import requests

from mlte.evidence.evidence_metadata import EvidenceMetadata
from mlte.value.types import Image

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
    local_path = str(download_image(tmp_path))
    _ = Image(EvidenceMetadata("typename", "id"), local_path)


def test_from_path(tmp_path):
    local_path = download_image(tmp_path)
    _ = Image(EvidenceMetadata("typename", "id"), local_path)


def test_from_bytes(tmp_path):
    local_path = download_image(tmp_path)

    with local_path.open("rb") as f:
        image = f.read()
    _ = Image(EvidenceMetadata("typename", "id"), image)


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_save_load(tmp_path):
    local_path = download_image(tmp_path)
    img = Image(EvidenceMetadata("typename", "id"), local_path)
    img.save()

    r: Image = Image.load("id")  # type: ignore
    assert r.image == r.image
