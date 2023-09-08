"""
test/fixture/artifact.py

Unit test support for artifact generation.
"""

from __future__ import annotations

import random
import string
from typing import Generator, List, Union

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.negotiation.model import NegotiationCardModel
from mlte.spec.model import SpecModel
from mlte.validation.model import ValidatedSpecModel
from mlte.value.model import IntegerValueModel, ValueModel, ValueType


def _random_id(length: int = 5) -> str:
    """
    Generate a random identifier.
    :param length: The length of the ID
    :return: The identifier
    """
    return "".join(random.choices(string.ascii_lowercase, k=length))


def artifact_types() -> Generator[ArtifactType, None, None]:
    """A generator over artifact types."""
    for type in ArtifactType:
        yield type


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
) -> Union[NegotiationCardModel, ValueModel, SpecModel, ValidatedSpecModel]:
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
    if type == ArtifactType.SPEC:
        return _make_spec()
    if type == ArtifactType.VALIDATED_SPEC:
        return _make_validated_spec()

    assert False, f"Unkown artifact type provided when creating body: {type}."


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


def _make_spec() -> SpecModel:
    """
    Make a minimal spec.
    :return: The artifact
    """
    return SpecModel(artifact_type=ArtifactType.SPEC)


def _make_validated_spec() -> ValidatedSpecModel:
    """
    Make a minimal validated spec.
    :return: The artifact
    """
    return ValidatedSpecModel(artifact_type=ArtifactType.VALIDATED_SPEC)
