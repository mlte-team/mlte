"""
mlte/artifact/artifact.py

Artifact protocol implementation.
"""

from __future__ import annotations

import abc
from typing import Optional

import mlte._private.meta as meta
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.session.session import session
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession
from mlte.store.query import Query, TypeFilter


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
        (model, version) and for a given artifact type.
        """

        self.type = type
        """The identifier for the artifact type"""

        self.timestamp = -1
        """The Unix timestamp of when the artifact was saved to a store."""

        self.creator = None
        """The user that created this artifact."""

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

    def _equal(a: Artifact, b: Artifact) -> bool:
        """
        Compare Artifact instances for equality.

        :param a: Input instance
        :param b: Input instance
        :return: `True` if `a` and `b` are equal, `False` otherwise
        """
        return a.to_model() == b.to_model()

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, Artifact):
            return False
        return self._equal(other)

    def __neq__(self, other: object) -> bool:
        """Test instance for inequality."""
        return not self.__eq__(other)

    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        A method that artifact subclasses can override to enforce pre-save invariants.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        # Default implementation is a no-op
        pass

    def post_load_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        A method that artifact subclasses may override to enforce post-load invariants.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        # Default implementation is a no-op
        pass

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
            session().context,
            session().artifact_store,
            force=force,
            parents=parents,
        )

    def save_with(
        self,
        context: Context,
        store: ArtifactStore,
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
        self.pre_save_hook(context, store)

        artifact_model = self.to_model()
        with ManagedArtifactSession(store.session()) as handle:
            handle.write_artifact_with_header(
                context.model,
                context.version,
                artifact_model,
                force=force,
                parents=parents,
            )

    @classmethod
    def load(cls, identifier: Optional[str] = None) -> Artifact:
        """
        Load an artifact from the configured global session.
        :param identifier: The identifier for the artifact

        This is equivalent to calling:
            Artifact.load_with(session().context, session().store)
        """
        return cls.load_with(
            identifier,
            context=session().context,
            store=session().artifact_store,
        )

    @classmethod
    def load_with(
        cls,
        identifier: Optional[str] = None,
        *,
        context: Context,
        store: ArtifactStore,
    ) -> Artifact:
        """
        Load an artifact with the given context and store configuration.
        :param identifier: The identifier for the artifact
        :param context: The context from which to load the artifact
        :param store: The store from which to load the artifact
        """
        if identifier is None:
            identifier = cls.get_default_id()

        with ManagedArtifactSession(store.session()) as handle:
            artifact = cls.from_model(
                handle.read_artifact(
                    context.model,
                    context.version,
                    identifier,
                )
            )

        artifact.post_load_hook(context, store)
        return artifact

    @staticmethod
    def load_all_models(artifact_type: ArtifactType) -> list[ArtifactModel]:
        """Loads all artifact models of the given type from the session."""
        return Artifact.load_all_models_with(
            artifact_type,
            context=session().context,
            store=session().artifact_store,
        )

    @staticmethod
    def load_all_models_with(
        artifact_type: ArtifactType, context: Context, store: ArtifactStore
    ) -> list[ArtifactModel]:
        """Loads all artifact models of the given type for the given context and store."""
        with ManagedArtifactSession(store.session()) as handle:
            query_instance = Query(filter=TypeFilter(item_type=artifact_type))
            artifact_models = handle.search_artifacts(
                context.model,
                context.version,
                query_instance,
            )
            return artifact_models

    @staticmethod
    def get_default_id() -> str:
        """To be overriden by derived classes."""
        return "default"

    def build_artifact_header(self) -> ArtifactHeaderModel:
        """Generates the common header model for artifacts."""
        return ArtifactHeaderModel(
            identifier=self.identifier,
            type=self.type,
            timestamp=self.timestamp,
            creator=self.creator,
        )
