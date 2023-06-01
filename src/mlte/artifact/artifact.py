"""
mlte/artifact/artifact.py

Artifact protocol implementation.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel

from mlte._global import global_state


class Artifact(BaseModel):
    """
    The MLTE artifact protocol implementation.

    The Artifact type establishes the common interface
    for all MLTE artifacts. This ensures that, even though
    they have very different semantics, all artifacts abide
    by a common protocol that allows us to perform common
    operations with them, namely persistence.
    """

    meta: ArtifactMeta
    """The artifact metadata."""

    def __init__(self, type: ArtifactType) -> None:
        global_state().ensure_initialized()
        model, version = global_state().get_model()

        self.meta = (
            ArtifactMeta.builder()
            .with_namespace(global_state().get_namespace())
            .with_model(model)
            .with_version(version)
            .with_type(type)
            .build()
        )


class ArtifactType(Enum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = "negotiation_card"
    """The negotiation card artifact type."""


class ArtifactMeta(BaseModel):
    """Common metadata for all MLTE artifacts."""

    namespace: str
    """The namespace with which the artifact is associated."""

    model: str
    """The identifier for the model with which the artifact is associated."""

    version: str
    """The identifier for the version with which the artifact is associated."""

    type: ArtifactType
    """The artifact type identifier."""

    @staticmethod
    def builder() -> ArtifactMetaBuilder:
        """
        Get a builder for ArtifactMeta.
        :return: The builder instance
        """
        return ArtifactMetaBuilder()


class ArtifactMetaBuilder:
    """A builder for artifact metadata."""

    def __init__(self) -> None:
        self._namespace: Optional[str] = None
        """The namespace with which the artifact is associated."""

        self._model: Optional[str] = None
        """The identifier for the model with which the artifact is associated."""

        self._version: Optional[str] = None
        """The identifier for the version with which the artifact is associated."""

        self._type: Optional[ArtifactType] = None
        """The artifact type identifier."""

    def with_namespace(self, namespace: str) -> ArtifactMetaBuilder:
        """
        Attach a namespace to artifact metadata.
        :param namespace: The namespace string
        :return: The builder
        """
        self._namespace = namespace
        return self

    def with_model(self, model: str) -> ArtifactMetaBuilder:
        """
        Attach a model identifier to artifact metadata.
        :param model: The model identifier
        :return: The builder
        """
        self._model = model
        return self

    def with_version(self, version: str) -> ArtifactMetaBuilder:
        """
        Attach a model version identifier to artifact metadata.
        :param version: The version identifier
        :return: The builder
        """
        self._version = version
        return self

    def with_type(self, type: ArtifactType) -> ArtifactMetaBuilder:
        """
        Attach an artifact type to artifact metadata.
        :param type: The artifact type identifier
        :return: The builder
        """
        self._type = type
        return self

    def build(self) -> ArtifactMeta:
        """
        Finalize the builder.
        :return: The artifact metadata instance
        """
        if self._namespace is None:
            raise ValueError("ArtifactMeta must specify namespace.")
        if self._model is None:
            raise ValueError("ArtifactMeta must specify model.")
        if self._version is None:
            raise ValueError("ArtifactMeta must specify version.")
        if self._type is None:
            raise ValueError("ArtifactMeta must specify type.")
        return ArtifactMeta(
            namespace=self._namespace,
            model=self._model,
            version=self._version,
            type=self._type,
        )
