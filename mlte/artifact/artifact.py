"""Artifact protocol implementation."""

from __future__ import annotations

import abc
import typing
from typing import Optional

from mlte.artifact.model import (
    ArtifactHeaderModel,
    ArtifactLevel,
    ArtifactModel,
)
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.model.serializable import Serializable
from mlte.session.session import session
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.query import Query, TypeFilter

DEFAULT_ID = "default"
"""Default id used if none is provided. Full id will be prefixed by type."""


class Artifact(Serializable, abc.ABC):
    """
    The MLTE artifact protocol implementation.

    The Artifact type establishes the common interface
    for all MLTE artifacts. This ensures that, even though
    they have very different semantics, all artifacts abide
    by a common protocol that allows us to perform common
    operations with them, namely persistence.
    """

    type: Optional[ArtifactType] = None
    """By default have no type, but a base Artifact should never be instantiated."""

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Main constructor for all artifacts."""

        self.identifier = self.build_full_id(identifier)
        """
        The identifier for the artifact, always having its type as prefix.
        An artifact identifier is unique within a MLTE context
        (model, version) and for a given artifact type.
        """

        self.timestamp = -1
        """The Unix timestamp of when the artifact was saved to a store."""

        self.creator = None
        """The user that created this artifact."""

        self.level = ArtifactLevel.VERSION
        """The artifact level, be it model or version, defaults to version."""

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, Artifact):
            return False
        return self._equal(other)

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

    def save(
        self,
        *,
        force: bool = False,
        parents: bool = False,
        user: Optional[str] = None,
    ) -> ArtifactModel:
        """
        Save an artifact with parameters from the configured global session.

        This is equivalent to calling:
            artifact.save_with(session().context, session().store)

        :param force: Indicates that an existing artifact may be overwritten
        :param parents: Indicates whether organizational elements for the
        artifact are created implicitly on write (default: False)
        :param user: The username of the user executing this action.
        :return: The ArtifactModel of the saved artifact.
        """
        return self.save_with(
            session().context,
            session().stores.artifact_store,
            force=force,
            parents=parents,
            user=user,
        )

    def save_with(
        self,
        context: Context,
        store: ArtifactStore,
        *,
        force: bool = False,
        parents: bool = False,
        user: Optional[str] = None,
    ) -> ArtifactModel:
        """
        Save an artifact with the given context and store configuration.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :param force: Indicates that an existing artifact may be overwritten
        :param parents: Indicates whether organizational elements for the
        artifact are created implicitly on write (default: False)
        :param user: The username of the user executing this action.
        :return: The ArtifactModel of the saved artifact.
        """
        with ManagedArtifactSession(store.session()) as artifact_store:
            # If we are forcing parent creation, ensure they are there before any hooks.
            if parents:
                artifact_store.create_parents(context.model, context.version)

            # Run any artifact-type specific pre save hooks.
            self.pre_save_hook(context, store)

            # Convert to model and save.
            model = self.to_model()

            # Run validation
            artifact_store.artifact_mapper.validators.validate_all()

            assert isinstance(
                model, ArtifactModel
            ), "Can't create object from non-ArtifactModel model."
            return artifact_store.artifact_mapper.write_artifact_with_header(
                context.model,
                context.version,
                model,
                force=force,
                user=user,
            )

    @classmethod
    def load(cls, identifier: Optional[str] = None) -> Artifact:
        """
        Load an artifact from the configured global session.
        :param identifier: The identifier for the artifact. If None,
        the default id is used.

        This is equivalent to calling:
            Artifact.load_with(session().context, session().store)
        """
        return cls.load_with(
            identifier,
            context=session().context,
            store=session().stores.artifact_store,
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
        :param identifier: The identifier for the artifact If None,
        the default id is used.
        :param context: The context from which to load the artifact
        :param store: The store from which to load the artifact
        """
        identifier = cls.build_full_id(identifier)

        with ManagedArtifactSession(store.session()) as artifact_store:
            artifact = typing.cast(
                Artifact,
                cls.from_model(
                    artifact_store.artifact_mapper.read(
                        identifier, (context.model, context.version)
                    )
                ),
            )

        artifact.post_load_hook(context, store)
        return artifact

    @staticmethod
    def load_models_for_session(
        artifact_type: ArtifactType,
    ) -> list[ArtifactModel]:
        """Loads all artifact models of the given type from the session."""
        return Artifact.load_models(
            artifact_type,
            context=session().context,
            store=session().stores.artifact_store,
        )

    @staticmethod
    def load_models(
        artifact_type: ArtifactType, context: Context, store: ArtifactStore
    ) -> list[ArtifactModel]:
        """Loads all artifact models of the given type for the given context and store."""
        with ManagedArtifactSession(store.session()) as artifact_store:
            query_instance = Query(filter=TypeFilter(item_type=artifact_type))
            artifact_models = artifact_store.artifact_mapper.search(
                query_instance, context=(context.model, context.version)
            )
            return artifact_models

    @classmethod
    def build_full_id(cls, base: Optional[str] = None) -> str:
        """Builds the full id for this artifact. If base is None, default base is used."""
        if not cls.type:
            raise RuntimeError(
                "Malformed artifact class, type has not been set."
            )
        if not base:
            base = DEFAULT_ID
        return Artifact._build_id(cls.type.value, base)

    @staticmethod
    def _build_id(prefix: str, base: str) -> str:
        """Builds the common id structure for an artifact."""
        if not base.startswith(f"{prefix}."):
            return f"{prefix}.{base}"
        else:
            return base

    def build_artifact_header(self) -> ArtifactHeaderModel:
        """Generates the common header model for artifacts."""
        if not self.type:
            raise RuntimeError(
                "Malformed artifact class, type has not been set."
            )
        return ArtifactHeaderModel(
            identifier=self.identifier,
            type=self.type,
            timestamp=self.timestamp,
            creator=self.creator,
            level=self.level,
        )

    def __str__(self) -> str:
        """Return a string representation."""
        return self.to_model().to_json_string()
