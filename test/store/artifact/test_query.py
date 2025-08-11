"""
test/store/artifact/test_query.py

Unit tests for store query functionality.
"""

import pytest

from mlte.artifact.type import ArtifactType
from mlte.store.query import (
    AllFilter,
    AndFilter,
    IdentifierFilter,
    NoneFilter,
    OrFilter,
    TypeFilter,
)

from ...fixture.artifact import ArtifactModelFactory, TypeUtil


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_all_match(artifact_type: ArtifactType) -> None:
    """The all filter matches all artifacts."""
    a = ArtifactModelFactory.make(artifact_type)
    assert AllFilter().match(a)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_none_match(artifact_type: ArtifactType) -> None:
    """The none filter matches no artifacts."""
    a = ArtifactModelFactory.make(artifact_type)
    assert not NoneFilter().match(a)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_identifier_match(artifact_type: ArtifactType) -> None:
    """The identifier filter matches the expected artifacts."""
    a = ArtifactModelFactory.make(artifact_type, "id0")
    b = ArtifactModelFactory.make(artifact_type, "id1")

    filter = IdentifierFilter(id="id0")
    assert filter.match(a)
    assert not filter.match(b)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_type_match(artifact_type: ArtifactType) -> None:
    """The type filter matches expected artifacts."""
    a = ArtifactModelFactory.make(artifact_type)

    filter = TypeFilter(item_type=artifact_type)
    assert filter.match(a)

    for type in TypeUtil.all_others(artifact_type):
        filter = TypeFilter(item_type=type)
        assert not filter.match(a)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_and_match(artifact_type: ArtifactType) -> None:
    """The and filter matches the expected artifacts."""
    a = ArtifactModelFactory.make(artifact_type, "id0")
    b = ArtifactModelFactory.make(artifact_type, "id1")

    filter = AndFilter(
        filters=[
            IdentifierFilter(id="id0"),
            TypeFilter(item_type=ArtifactType.NEGOTIATION_CARD),
        ],
    )

    if a.header.type == ArtifactType.NEGOTIATION_CARD:
        assert filter.match(a)
    else:
        assert not filter.match(a)
    assert not filter.match(b)


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_or_match(artifact_type: ArtifactType) -> None:
    """The or filter matches the expected artifacts."""
    a = ArtifactModelFactory.make(artifact_type, "id0")
    b = ArtifactModelFactory.make(artifact_type, "id1")
    c = ArtifactModelFactory.make(artifact_type, "id3")

    filter = OrFilter(
        filters=[
            IdentifierFilter(id="id0"),
            IdentifierFilter(id="id1"),
        ],
    )

    assert filter.match(a)
    assert filter.match(b)
    assert not filter.match(c)
