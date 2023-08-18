"""
test/fixture/artifact.py

Unit test support for artifact generation.
"""

from __future__ import annotations

import random
import string
from typing import List, Union

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.identifier import Identifier
from mlte.evidence.metadata import EvidenceMetadata
from mlte.negotiation.model import NegotiationCardModel
from mlte.value.model import IntegerValueModel, ValueModel, ValueType


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
            body=_make_body(type, id),
        )


class TypeUtil:
    """A static class for artifact type utilities."""

    @staticmethod
    def all_others(type: ArtifactType) -> List[ArtifactType]:
        """
        Return a collection of all artifact types that are not the given one.
        :param type: The excluded type
        :return: The included types
        """
        return [t for t in ArtifactType if t != type]


def _make_body(
    type: ArtifactType, id: str
) -> Union[NegotiationCardModel, ValueModel]:
    """
    Make the body of the artifact for a given type.
    :param type: The artifact type
    :param id: The identifier for the artifact
    :return: The artifact body model
    """
    if type == ArtifactType.NEGOTIATION_CARD:
        return _make_negotiation_card()
    if type == ArtifactType.VALUE:
        return _make_value(id)
    assert False, "Unreachable."


def _make_negotiation_card() -> NegotiationCardModel:
    """
    Make a minimal negotiation card.
    :return: The artifact
    """
    return NegotiationCardModel(artifact_type=ArtifactType.NEGOTIATION_CARD)


def _make_value(id: str) -> ValueModel:
    """
    Make a minimal value.
    :return: The artifact
    """
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name=id)
    )
    return ValueModel(
        artifact_type=ArtifactType.VALUE,
        metadata=m,
        value=IntegerValueModel(value_type=ValueType.INTEGER, integer=1),
    )
