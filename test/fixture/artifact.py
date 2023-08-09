"""
test/fixture/artifact.py

Unit test support for artifact generation.
"""

import random
import string

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.negotiation.model import NegotiationCardModel


def _random_id(length: int = 5) -> str:
    """
    Generate a random identifier.
    :param length: The length of the ID
    :return: The identifier
    """
    return "".join(random.choices(string.ascii_lowercase, k=length))


class ArtifactFactory:
    """A class for build artifacts."""

    @staticmethod
    def make(type: ArtifactType, id: str = _random_id()) -> ArtifactModel:
        """
        Construct an artifact model of the given type.
        :param type: The artifact type
        :param id: The artifact identifier (default: randomly generated)
        :return: The artifact model
        """
        return ArtifactModel(
            header=ArtifactHeaderModel(identifier=id, type=type),
            body=_make_body(type),
        )


class TypeUtil:
    """A static class for artifact type utilities."""

    @staticmethod
    def all_others(type: ArtifactType) -> list[ArtifactType]:
        """
        Return a collection of all artifact types that are not the given one.
        :param type: The excluded type
        :return: The included types
        """
        return [t for t in ArtifactType if t != type]


def _make_body(type: ArtifactType) -> NegotiationCardModel:
    """
    Make the body of the artifact for a given type.
    :param type: The artifact type
    :return: The artifact body model
    """
    if type == ArtifactType.NEGOTIATION_CARD:
        return _make_negotiation_card()
    assert False, "Unreachable."


def _make_negotiation_card() -> NegotiationCardModel:
    """
    Make a minimal negotiation card.
    :return: The artifact
    """
    return NegotiationCardModel()
