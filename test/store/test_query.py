"""
test/store/test_query.py

Unit tests for store query functionality.
"""

import pytest

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.query import (
    AllFilter,
    AndFilter,
    ArtifactIdentifierFilter,
    ArtifactTypeFilter,
    FilterType,
    NoneFilter,
    OrFilter,
)

# TODO(Kyle): Make these parametric over artifact types.


def test_all() -> None:
    """The all filter can be serialized and deserialized."""
    f = AllFilter(type=FilterType.ALL)
    assert AllFilter(**f.dict()) == f


@pytest.mark.skip("Make parametric.")
def test_all_match() -> None:
    """The all filter matches all artifacts."""
    a = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )
    assert AllFilter(type=FilterType.ALL).match(a)


def test_none() -> None:
    """The all filter cna be serialized and deserialized."""
    f = NoneFilter(type=FilterType.NONE)
    assert NoneFilter(**f.dict()) == f


@pytest.mark.skip("Make parametric.")
def test_none_match() -> None:
    """The none filter matches no artifacts."""
    a = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )
    assert not NoneFilter(type=FilterType.NONE).match(a)


def test_identifier() -> None:
    """The identifier filter can be serialized and deserialized."""
    f = ArtifactIdentifierFilter(type=FilterType.IDENTIFIER, artifact_id="id0")
    assert ArtifactIdentifierFilter(**f.dict()) == f


@pytest.mark.skip("Make parametric.")
def test_identifier_match() -> None:
    """The identifier filter matches the expected artifacts."""
    a = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id0", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )
    b = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id1", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )

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
    assert ArtifactTypeFilter(**f.dict()) == f


@pytest.mark.skip("Make parametric.")
def test_type_match() -> None:
    """The type filter matches expected artifacts."""
    a = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id0", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )
    filter = ArtifactTypeFilter(
        type=FilterType.TYPE, artifact_type=ArtifactType.NEGOTIATION_CARD
    )
    assert filter.match(a)


def test_and() -> None:
    """The AND filter can be serialized and deserialized."""
    f = AndFilter(
        type=FilterType.AND,
        filters=[
            AllFilter(type=FilterType.ALL),
            NoneFilter(type=FilterType.NONE),
        ],
    )
    assert AndFilter(**f.dict()) == f


@pytest.mark.skip("Make parametric.")
def test_and_match() -> None:
    """The AND filter matches expected artifacts."""
    filter = AndFilter(
        type=FilterType.AND,
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
    assert str(filter) == "identifier=id0 and type=negotiation_card"


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
    assert OrFilter(**f.dict()) == f
