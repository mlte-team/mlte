"""
test/store/test_query.py

Unit tests for store query functionality.
"""

import pytest

from mlte.artifact.type import ArtifactType
from mlte.store.artifact.query import (
    ArtifactIdentifierFilter,
    ArtifactTypeFilter,
)
from mlte.store.common.query import (
    AllFilter,
    AndFilter,
    FilterType,
    NoneFilter,
    OrFilter,
)

from ...fixture.artifact import ArtifactFactory, TypeUtil


def test_all() -> None:
    """The all filter can be serialized and deserialized."""
    f = AllFilter(type=FilterType.ALL)
    assert AllFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_all_match(artifact_type: ArtifactType) -> None:
    """The all filter matches all artifacts."""
    a = ArtifactFactory.make(artifact_type)
    assert AllFilter(type=FilterType.ALL).match(a)


def test_none() -> None:
    """The all filter cna be serialized and deserialized."""
    f = NoneFilter(type=FilterType.NONE)
    assert NoneFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_none_match(artifact_type: ArtifactType) -> None:
    """The none filter matches no artifacts."""
    a = ArtifactFactory.make(artifact_type)
    assert not NoneFilter(type=FilterType.NONE).match(a)


def test_identifier() -> None:
    """The identifier filter can be serialized and deserialized."""
    f = ArtifactIdentifierFilter(type=FilterType.IDENTIFIER, artifact_id="id0")
    assert ArtifactIdentifierFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_identifier_match(artifact_type: ArtifactType) -> None:
    """The identifier filter matches the expected artifacts."""
    a = ArtifactFactory.make(artifact_type, "id0")
    b = ArtifactFactory.make(artifact_type, "id1")

    filter = ArtifactIdentifierFilter(
        type=FilterType.IDENTIFIER, artifact_id="id0"
    )
    assert filter.match(a)
    assert not filter.match(b)


def test_type() -> None:
    """The type filter can be serialized and deserialized."""
    f = ArtifactTypeFilter(
        type=FilterType.TYPE, artifact_type=ArtifactType.NEGOTIATION_CARD
    )
    assert ArtifactTypeFilter(**f.model_dump()) == f


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_type_match(artifact_type: ArtifactType) -> None:
    """The type filter matches expected artifacts."""
    a = ArtifactFactory.make(artifact_type)

    filter = ArtifactTypeFilter(
        type=FilterType.TYPE, artifact_type=artifact_type
    )
    assert filter.match(a)

    for type in TypeUtil.all_others(artifact_type):
        filter = ArtifactTypeFilter(type=FilterType.TYPE, artifact_type=type)
        assert not filter.match(a)


def test_and() -> None:
    """The AND filter can be serialized and deserialized."""
    f = AndFilter(
        type=FilterType.AND,
        filters=[
            AllFilter(type=FilterType.ALL),
            NoneFilter(type=FilterType.NONE),
        ],
    )
    assert AndFilter(**f.model_dump()) == f


@pytest.mark.skip("Implement.")
def test_and_match() -> None:
    assert True


def test_or() -> None:
    """The OR filter can be serialized and deserialized."""
    f = OrFilter(
        type=FilterType.OR,
        filters=[
            ArtifactIdentifierFilter(
                type=FilterType.IDENTIFIER, artifact_id="id0"
            ),
            ArtifactTypeFilter(
                type=FilterType.TYPE,
                artifact_type=ArtifactType.NEGOTIATION_CARD,
            ),
        ],
    )
    assert OrFilter(**f.model_dump()) == f


@pytest.mark.skip("Implement.")
def test_or_match() -> None:
    assert True
