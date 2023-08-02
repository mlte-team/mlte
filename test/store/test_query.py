"""
test/store/test_query.py

Unit tests for store query functionality.
"""

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.query import AllFilter, ArtifactIdentifierFilter, NoneFilter

# TODO(Kyle): Make these parametric over artifact types.


def test_all() -> None:
    """The all filter matches all artifacts."""
    a = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )
    assert AllFilter().match(a)


def test_none() -> None:
    """The all filter matches all artifacts."""
    a = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )
    assert not NoneFilter().match(a)


def test_identifier() -> None:
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

    filter = ArtifactIdentifierFilter(artifact_id="id0")
    assert filter.match(a)
    assert not filter.match(b)
