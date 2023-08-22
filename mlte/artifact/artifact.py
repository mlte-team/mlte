"""
mlte/artifact/artifact.py

Artifact protocol implementation.
"""

from __future__ import annotations

import abc

import mlte._private.meta as meta
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.session.state import session
from mlte.store.base import ManagedSession, Store


class Artifact(metaclass=abc.ABCMeta):
    """
    The MLTE artifact protocol implementation.

    The Artifact type establishes the common interface
    for all MLTE artifacts. This ensures that, even though
    they have very different semantics, all artifacts abide
    by a common protocol that allows us to perform common
    operations with them, namely persistence.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return meta.has_callables(subclass, "to_model", "from_model")

    def __init__(self, identifier: str, type: ArtifactType) -> None:
        self.identifier = identifier
        """
        The identifier for the artifact.
        An artifact identifier is unique within a MLTE context
        (namespace, model, version) and for a given artifact type.
        """

        self.type = type
        """The identifier for the artifact type"""

    @abc.abstractmethod
    def to_model(self) -> ArtifactModel:
        """Serialize an artifact to its corresponding model."""
        raise NotImplementedError(
            "Artifact.to_model() not implemented for abstract Artifact."
        )

    @classmethod
    @abc.abstractmethod
    def from_model(cls, _: ArtifactModel) -> Artifact:
        """Deserialize an artifact from its corresponding model."""
        raise NotImplementedError(
            "Artifact.from_model() not implemented for abstract Artifact."
        )

    def save(self, *, force: bool = False, parents: bool = False) -> None:
        """
        Save an artifact with parameters from the configured global session.

        This is equivalent to calling:
            artifact.save_with(session().context, session().store)

        :param force: Indicates that an existing artifact may be overwritten
        :param parents: Indicates whether organizational elements for the
        artifact are created implicitly on write (default: False)
        """
        self.save_with(
            session().context, session().store, force=force, parents=parents
        )

    def save_with(
        self,
        context: Context,
        store: Store,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> None:
        """
        Save an artifact with the given context and store configuration.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :param force: Indicates that an existing artifact may be overwritten
        :param parents: Indicates whether organizational elements for the
        artifact are created implicitly on write (default: False)
        """
        with ManagedSession(store.session()) as handle:
            handle.write_artifact(
                context.namespace,
                context.model,
                context.version,
                self.to_model(),
                force=force,
                parents=parents,
            )

    @classmethod
    def load(cls, identifier: str) -> Artifact:
        """
        Load an artifact from the configured global session.
        :param identifier: The identifier for the artifact

        This is equivalent to calling:
            Artifact.load_with(session().context, session().store)
        """
        return cls.load_with(identifier, session().context, session().store)

    @classmethod
    def load_with(
        cls, identifier: str, context: Context, store: Store
    ) -> Artifact:
        """
        Load an artifact with the given context and store configuration.
        :param identifier: The identifier for the artifact
        :param context: The context from which to load the artifact
        :param store: The store from which to load the artifact
        """
        with ManagedSession(store.session()) as handle:
            return cls.from_model(
                handle.read_artifact(
                    context.namespace,
                    context.model,
                    context.version,
                    identifier,
                )
            )
