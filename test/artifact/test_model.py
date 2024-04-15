"""
test/artifact/test_model.py

Unit tests for artifact models.
"""

import pydantic
import pytest

from mlte.artifact.model import ArtifactHeaderModel
from mlte.artifact.type import ArtifactType


def test_negotiation_card_header() -> None:
    """A negotiation header body model can be serialized and deserialized."""
    objects = [
        ArtifactHeaderModel(
            identifier="identifier",
            type=ArtifactType.NEGOTIATION_CARD,
            creator="user1",
        )
    ]
    for object in objects:
        s = object.to_json()
        d = ArtifactHeaderModel.from_json(s)
        assert d == object

    with pytest.raises(pydantic.ValidationError):
        _ = ArtifactHeaderModel(identifier="identifier")  # type: ignore

    with pytest.raises(pydantic.ValidationError):
        _ = ArtifactHeaderModel(type=ArtifactType.NEGOTIATION_CARD)  # type: ignore

    with pytest.raises(pydantic.ValidationError):
        _ = ArtifactHeaderModel(creator="user1")  # type: ignore
