"""
mlte/store/underlying/memory.py

Implementation of in-memory artifact store.
"""

from contextlib import contextmanager

from mlte.store.store import Store, StoreSession, StoreURI
from mlte.context.model import Namespace, Model, Version
from mlte.negotiation.model import NegotiationCardModel

import mlte.store.error as errors

# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class VersionWithArtifacts:
    """A structure that combines a version with the artifacts it contains."""

    def __init__(self, *, version: Version) -> None:
        self.version = version
        """The version object."""

        self.negotiation_cards: dict[str, NegotiationCardModel] = {}
        """The negotiation card models associated with the version."""


class ModelWithVersions:
    """A structure that combines a model with the versions it contains."""

    def __init__(self, *, model: Model) -> None:
        self.model = model
        """The model object."""

        self.versions: dict[str, VersionWithArtifacts] = {}
        """The collection of versions in the namespace."""


class NamespaceWithModels:
    """A structure that combines a namespace with the models it contains."""

    def __init__(self, *, namespace: Namespace) -> None:
        self.namespace = namespace
        """The namespace object."""

        self.models: dict[str, ModelWithVersions] = {}
        """The collection of models in the namespace."""


# -----------------------------------------------------------------------------
# InMemoryStoreSession
# -----------------------------------------------------------------------------


class InMemoryStoreSession(StoreSession):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, *, storage: dict[str, NamespaceWithModels]) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        # NOTE(Kyle): Closing an in-memory session is a no-op.
        pass

    def create_namespace(self, namespace: Namespace) -> None:
        if namespace.identifier in self.storage:
            raise errors.ErrorAlreadyExists(f"Namespace {namespace.identifier}")

        self.storage[namespace.identifier] = NamespaceWithModels(
            namespace=namespace
        )

    def read_namespace(self, namespace_id: str) -> list[Model]:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")
        return [item.model for item in self.storage[namespace_id].models]

    def delete_namespace(self, namespace_id: str) -> None:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")
        del self.storage[namespace_id]

    def create_model(self, namespace_id: str, model: Model) -> None:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage[namespace_id]
        if model.identifier in namespace.models:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")

        namespace.models[model.identifier] = ModelWithVersions(model=model)

    def read_model(self, namespace_id: str, model_id: str) -> list[Version]:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        return namespace.models[model_id].model

    def delete_model(self, namespace_id: str, model_id: str) -> None:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        del namespace.models[model_id]

    def create_version(
        self, namespace_id: str, model_id: str, version: Version
    ) -> None:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version.identifier in model.versions:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")

        model.versions[version.identifier] = VersionWithArtifacts(
            version=version
        )

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return model.versions[version_id].version

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> None:
        """
        Delete a MLTE model version.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        """
        if namespace_id not in self.storage:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        del model.versions[version_id]


class InMemoryStore(Store):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage: dict[str, NamespaceWithModels] = {}
        """The underlying storage for the store."""

    @contextmanager
    def session(self) -> InMemoryStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        session = InMemoryStoreSession(storage=self.storage)
        try:
            yield session
        finally:
            session.close()
