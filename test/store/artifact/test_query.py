"""
test/store/artifact/test_query.py

Unit tests for store query functionality.
"""

import pytest

from mlte.artifact.type import ArtifactType
from mlte.store.artifact.query import (
    ArtifactAndFilter,
    ArtifactIdentifierFilter,
    ArtifactOrFilter,
    ArtifactTypeFilter,
)
from mlte.store.query import AllFilter, NoneFilter

from ...fixture.artifact import ArtifactFactory, TypeUtil


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_all_match(artifact_type: ArtifactType) -> None:
    """The all filter matches all artifacts."""
    a = ArtifactFactory.make(artifact_type)
    assert AllFilter().match(a)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_none_match(artifact_type: ArtifactType) -> None:
    """The none filter matches no artifacts."""
    a = ArtifactFactory.make(artifact_type)
    assert not NoneFilter().match(a)


def test_identifier() -> None:
    """The identifier filter can be serialized and deserialized."""
    f = ArtifactIdentifierFilter(artifact_id="id0")
    assert ArtifactIdentifierFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_identifier_match(artifact_type: ArtifactType) -> None:
    """The identifier filter matches the expected artifacts."""
    a = ArtifactFactory.make(artifact_type, "id0")
    b = ArtifactFactory.make(artifact_type, "id1")

    filter = ArtifactIdentifierFilter(artifact_id="id0")
    assert filter.match(a)
    assert not filter.match(b)


def test_type() -> None:
    """The type filter can be serialized and deserialized."""
    f = ArtifactTypeFilter(artifact_type=ArtifactType.NEGOTIATION_CARD)
    assert ArtifactTypeFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_type_match(artifact_type: ArtifactType) -> None:
    """The type filter matches expected artifacts."""
    a = ArtifactFactory.make(artifact_type)

    filter = ArtifactTypeFilter(artifact_type=artifact_type)
    assert filter.match(a)

    for type in TypeUtil.all_others(artifact_type):
        filter = ArtifactTypeFilter(artifact_type=type)
        assert not filter.match(a)


def test_and() -> None:
    """The AND filter can be serialized and deserialized."""
    f = ArtifactAndFilter(
        filters=[
            AllFilter(),
            NoneFilter(),
            ArtifactIdentifierFilter(artifact_id="id0"),
            ArtifactTypeFilter(artifact_type=ArtifactType.NEGOTIATION_CARD),
        ],
    )
    assert ArtifactAndFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_and_match(artifact_type: ArtifactType) -> None:
    """The and filter matches the expected artifacts."""
    a = ArtifactFactory.make(artifact_type, "id0")
    b = ArtifactFactory.make(artifact_type, "id1")

    filter = ArtifactAndFilter(
        filters=[
            ArtifactIdentifierFilter(artifact_id="id0"),
            ArtifactTypeFilter(artifact_type=ArtifactType.NEGOTIATION_CARD),
        ],
    )

    if a.header.type == ArtifactType.NEGOTIATION_CARD:
        assert filter.match(a)
    else:
        assert not filter.match(a)
    assert not filter.match(b)


def test_or() -> None:
    """The OR filter can be serialized and deserialized."""
    f = ArtifactOrFilter(
        filters=[
            AllFilter(),
            NoneFilter(),
            ArtifactIdentifierFilter(artifact_id="id0"),
            ArtifactTypeFilter(artifact_type=ArtifactType.NEGOTIATION_CARD),
        ],
    )
    assert ArtifactOrFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_or_match(artifact_type: ArtifactType) -> None:
    """The or filter matches the expected artifacts."""
    a = ArtifactFactory.make(artifact_type, "id0")
    b = ArtifactFactory.make(artifact_type, "id1")
    c = ArtifactFactory.make(artifact_type, "id3")

    filter = ArtifactOrFilter(
        filters=[
            ArtifactIdentifierFilter(artifact_id="id0"),
            ArtifactIdentifierFilter(artifact_id="id1"),
        ],
    )

    assert filter.match(a)
    assert filter.match(b)
    assert not filter.match(c)
