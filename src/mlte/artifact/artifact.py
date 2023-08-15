"""
mlte/artifact/artifact.py

Artifact protocol implementation.
"""

from __future__ import annotations

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context import Context
from mlte.session import session
from mlte.store import ManagedSession, Store


class Artifact:
    """
    The MLTE artifact protocol implementation.

    The Artifact type establishes the common interface
    for all MLTE artifacts. This ensures that, even though
    they have very different semantics, all artifacts abide
    by a common protocol that allows us to perform common
    operations with them, namely persistence.
    """

    def __init__(self, identifier: str, type: ArtifactType) -> None:
        self.identifier = identifier
        """
        The identifier for the artifact.
        An artifact identifier is unique within a MLTE context
        (namespace, model, version) and for a given artifact type.
        """

        self.type = type
        """The identifier for the artifact type"""

    def to_model(self) -> ArtifactModel:
        """Serialize an artifact to its corresponding model."""
        raise NotImplementedError(
            "Artifact.to_model() not implemented for abstract Artifact."
        )

    @staticmethod
    def from_model(_: ArtifactModel) -> Artifact:
        """Deserialize an artifact from its corresponding model."""
        raise NotImplementedError(
            "Artifact.from_model() not implemented for abstract Artifact."
        )

    def save(self) -> None:
        """
        Save an artifact with parameters from the configured global session.

        This is equivalent to calling:
            artifact.save_with(session().context, session().store)
        """
        self.save_with(session().context, session().store)

    def save_with(self, context: Context, store: Store) -> None:
        """
        Save an artifact with the given context and store configuration.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        """
        with ManagedSession(store.session()) as handle:
            handle.write_artifact(
                context.namespace,
                context.model,
                context.version,
                self.to_model(),
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
