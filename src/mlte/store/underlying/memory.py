"""
mlte/store/underlying/memory.py

Implementation of in-memory artifact store.
"""

from mlte.store.store import Store, StoreSession, StoreURI
from mlte.context.model import (
    Namespace,
    Model,
    Version,
    NamespaceCreate,
    ModelCreate,
    VersionCreate,
)
from mlte.negotiation.model import NegotiationCardModel

import mlte.store.error as errors

# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class VersionWithArtifacts:
    """A structure that combines a version with the artifacts it contains."""

    def __init__(self, *, identifier: str) -> None:
        self.identifier = identifier
        """The version identifier."""

        self.negotiation_cards: dict[str, NegotiationCardModel] = {}
        """The negotiation card models associated with the version."""


class ModelWithVersions:
    """A structure that combines a model with the versions it contains."""

    def __init__(self, *, identifier: str) -> None:
        self.identifier = identifier
        """The model identifier."""

        self.versions: dict[str, VersionWithArtifacts] = {}
        """The collection of versions in the namespace."""


class NamespaceWithModels:
    """A structure that combines a namespace with the models it contains."""

    def __init__(self, *, identifier: str) -> None:
        self.identifier = identifier
        """The namespace identifier."""

        self.models: dict[str, ModelWithVersions] = {}
        """The collection of models in the namespace."""


class Storage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.namespaces: dict[str, NamespaceWithModels] = {}


# -----------------------------------------------------------------------------
# InMemoryStoreSession
# -----------------------------------------------------------------------------


class InMemoryStoreSession(StoreSession):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, *, storage: Storage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        # NOTE(Kyle): Closing an in-memory session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        if namespace.identifier in self.storage.namespaces:
            raise errors.ErrorAlreadyExists(f"Namespace {namespace.identifier}")
        self.storage.namespaces[namespace.identifier] = NamespaceWithModels(
            identifier=namespace.identifier
        )
        return Namespace(identifier=namespace.identifier, models=[])

    def read_namespace(self, namespace_id: str) -> Namespace:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")
        return self._read_namespace(namespace_id)

    def list_namespaces(self) -> list[str]:
        return [ns_id for ns_id in self.storage.namespaces.keys()]

    def delete_namespace(self, namespace_id: str) -> Namespace:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        popped = self._read_namespace(namespace_id)
        del self.storage.namespaces[namespace_id]
        return popped

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model.identifier in namespace.models:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")

        namespace.models[model.identifier] = ModelWithVersions(
            identifier=model.identifier
        )
        return Model(identifier=model.identifier, versions=[])

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")
        return self._read_model(namespace_id, model_id)

    def list_models(self, namespace_id: str) -> list[str]:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        return [model_id for model_id in namespace.models.keys()]

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        popped = self._read_model(namespace_id, model_id)
        del namespace.models[model_id]
        return popped

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version.identifier in model.versions:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")

        model.versions[version.identifier] = VersionWithArtifacts(
            identifier=version.identifier
        )
        return Version(identifier=version.identifier)

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return self._read_version(namespace_id, model_id, version_id)

    def list_versions(self, namespace_id: str, model_id: str) -> list[str]:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        return [version_id for version_id in model.versions.keys()]

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        popped = self._read_version(namespace_id, model_id, version_id)
        del model.versions[version_id]
        return popped

    def _read_namespace(self, namespace_id: str) -> Namespace:
        """
        Lazily construct a Namespace object on read.
        :param namespace_id: The namespace identifer
        :return: The Namespace object
        """
        assert namespace_id in self.storage.namespaces, "Broken precondition."
        return Namespace(
            identifier=namespace_id,
            models=[
                self._read_model(namespace_id, id)
                for id in self.storage.namespaces[namespace_id].models.keys()
            ],
        )

    def _read_model(self, namespace_id: str, model_id: str) -> Model:
        """
        Lazily construct a Model object on read.
        :param namespace_id: The namespace identifier
        :param model_id: The model identifier
        :return: The model object
        """
        assert namespace_id in self.storage.namespaces, "Broken precondition."
        assert (
            model_id in self.storage.namespaces[namespace_id].models
        ), "Broken precondition."
        return Model(
            identifier=model_id,
            versions=[
                self._read_version(namespace_id, model_id, id)
                for id in self.storage.namespaces[namespace_id]
                .models[model_id]
                .versions.keys()
            ],
        )

    def _read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        """
        Lazily construct a Version object on read.
        :param namespace_id: The namespace identifier
        :param model_id: The model identifier
        :param version_id: The version identifier
        :return: The version object
        """
        assert namespace_id in self.storage.namespaces, "Broken precondition."
        assert (
            model_id in self.storage.namespaces[namespace_id].models
        ), "Broken precondition."
        assert (
            version_id
            in self.storage.namespaces[namespace_id].models[model_id].versions
        ), "Broken precondition."
        return Version(
            identifier=self.storage.namespaces[namespace_id]
            .models[model_id]
            .versions[version_id]
            .identifier
        )

    # -------------------------------------------------------------------------
    # Negotiation Card
    # -------------------------------------------------------------------------

    def write_negotiation_card(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact: NegotiationCardModel,
    ) -> NegotiationCardModel:
        version = self._get_version_with_artifacts(
            namespace_id, model_id, version_id
        )

        if artifact.header.identifier in version.negotiation_cards:
            raise errors.ErrorAlreadyExists(
                f"NegotiationCard '{artifact.header.identifier}'"
            )
        version.negotiation_cards[artifact.header.identifier] = artifact
        return artifact

    def read_negotiation_card(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> NegotiationCardModel:
        version = self._get_version_with_artifacts(
            namespace_id, model_id, version_id
        )

        if artifact_id not in version.negotiation_cards:
            raise errors.ErrorNotFound(f"NegotiationCard '{artifact_id}'")
        return version.negotiation_cards[artifact_id]

    def delete_negotiation_card(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> NegotiationCardModel:
        version = self._get_version_with_artifacts(
            namespace_id, model_id, version_id
        )

        if artifact_id not in version.negotiation_cards:
            raise errors.ErrorNotFound(f"NegotiationCard '{artifact_id}'")
        artifact = version.negotiation_cards[artifact_id]
        del version.negotiation_cards[artifact_id]
        return artifact

    def _get_version_with_artifacts(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> VersionWithArtifacts:
        """
        Get a version with artifacts from storage.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the version
        :raises ErrorNotFound: If the required structural elements are not present
        :return: The version with associated artifacts
        """
        if namespace_id not in self.storage.namespaces:
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

        namespace = self.storage.namespaces[namespace_id]
        if model_id not in namespace.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = namespace.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return model.versions[version_id]


class InMemoryStore(Store):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = Storage()
        """The underlying storage for the store."""

    def session(self) -> InMemoryStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryStoreSession(storage=self.storage)
