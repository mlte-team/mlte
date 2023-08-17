"""
mlte/store/underlying/fs.py

Implementation of local file system artifact store.
"""


from typing import Any
from pathlib import Path
import json
import shutil

from mlte.store.store import Store, StoreSession, StoreURI
from mlte.context.model import (
    Namespace,
    Model,
    Version,
    NamespaceCreate,
    ModelCreate,
    VersionCreate,
)
from mlte.artifact.model import ArtifactModel
from mlte.store.query import Query

import mlte.store.error as errors


# The prefix that indicates a local filesystem directory is used
LOCAL_URI_PREFIX = "local://"
FS_URI_PREFIX = "fs://"


def _parse_root_path(uristr: str) -> Path:
    """
    Parse the root path for the backend from the URI.
    :param uri: The URI
    :type uri: str
    :return: The parsed path
    :rtype: Path
    """
    assert uristr.startswith(FS_URI_PREFIX) or uristr.startswith(
        LOCAL_URI_PREFIX
    ), "Broken precondition."
    prefix = (
        FS_URI_PREFIX if uristr.startswith(FS_URI_PREFIX) else LOCAL_URI_PREFIX
    )
    return Path(uristr[len(prefix) :])


class JsonFileStorage:
    """A simple JSON storage wrapper for the file system store."""

    def create_folder(self, path: Path) -> None:
        Path.mkdir(path, parents=True)

    def list_folders(self, path: Path) -> list[Path]:
        return [x for x in sorted(path.iterdir()) if x.is_dir()]

    def delete_folder(self, path: Path) -> None:
        shutil.rmtree(path)

    def list_json_files(self, path: Path) -> list[Path]:
        return [
            x
            for x in sorted(path.iterdir())
            if x.is_file() and x.suffix == ".json"
        ]

    def read_json_file(self, path: Path) -> dict[str, Any]:
        with path.open("r") as f:
            data: dict[str, Any] = json.load(f)
        return data

    def write_json_to_file(self, path: Path, data: dict[str, Any]) -> None:
        with path.open("w") as f:
            json.dump(data, f, indent=4)

    def delete_file(self, path: Path) -> None:
        if not path.exists():
            raise RuntimeError(f"Path {path} does not exist.")
        path.unlink()


# -----------------------------------------------------------------------------
# LocalFileSystemStoreSession
# -----------------------------------------------------------------------------


class LocalFileSystemStoreSession(StoreSession):
    """A local file-system implementation of the MLTE artifact store."""

    def __init__(self, uri: str, storage: JsonFileStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.root = _parse_root_path(uri)
        """The remote artifact store URL."""

        if not self.root.exists():
            raise FileNotFoundError(
                f"Root data storage location does not exist: {self.root}."
            )

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        try:
            self.storage.create_folder(Path(self.root, namespace.identifier))
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Namespace {namespace.identifier}")
        return Namespace(identifier=namespace.identifier, models=[])

    def read_namespace(self, namespace_id: str) -> Namespace:
        self._ensure_namespace_exists(namespace_id)
        return self._read_namespace(namespace_id)

    def list_namespaces(self) -> list[str]:
        return [
            str(ns_folder)
            for ns_folder in self.storage.list_folders(Path(self.root))
        ]

    def delete_namespace(self, namespace_id: str) -> Namespace:
        self._ensure_namespace_exists(namespace_id)
        namespace = self._read_namespace(namespace_id)
        self.storage.delete_folder(Path(self.root, namespace_id))
        return namespace

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        self._ensure_namespace_exists(namespace_id)

        try:
            self.storage.create_folder(
                Path(self.root, namespace_id, model.identifier)
            )
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")

        return Model(identifier=model.identifier, versions=[])

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)
        return self._read_model(namespace_id, model_id)

    def list_models(self, namespace_id: str) -> list[str]:
        self._ensure_namespace_exists(namespace_id)
        return [
            str(model_folder)
            for model_folder in self.storage.list_folders(
                Path(self.root, namespace_id)
            )
        ]

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)

        model = self._read_model(namespace_id, model_id)
        self.storage.delete_folder(Path(self.root, namespace_id, model_id))
        return model

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)

        try:
            self.storage.create_folder(
                Path(self.root, namespace_id, model_id, version.identifier)
            )
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")
        return Version(identifier=version.identifier)

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)
        self._ensure_version_exists(namespace_id, model_id, version_id)

        return self._read_version(namespace_id, model_id, version_id)

    def list_versions(self, namespace_id: str, model_id: str) -> list[str]:
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)

        return [
            str(version_folder)
            for version_folder in self.storage.list_folders(
                Path(self.root, namespace_id, model_id)
            )
        ]

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)
        self._ensure_version_exists(namespace_id, model_id, version_id)

        version = self._read_version(namespace_id, model_id, version_id)
        self.storage.delete_folder(
            Path(self.root, namespace_id, model_id, version_id)
        )
        return version

    def _ensure_namespace_exists(self, namespace_id: str) -> None:
        """Throws an ErrorNotFound if the given namespace does not exist."""
        if not Path(self.root, namespace_id).exists():
            raise errors.ErrorNotFound(f"Namespace {namespace_id}")

    def _ensure_model_exists(self, namespace_id: str, model_id: str) -> None:
        """Throws an ErrorNotFound if the given model in the given namespace does not exist."""
        if not Path(self.root, namespace_id, model_id).exists():
            raise errors.ErrorNotFound(
                f"Model {model_id} in namespace {namespace_id}"
            )

    def _ensure_version_exists(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> None:
        """Throws an ErrorNotFound if the given version of the given model in the given namespace does not exist."""
        if not Path(self.root, namespace_id, model_id, version_id).exists():
            raise errors.ErrorNotFound(
                f"Version {version_id} in model {model_id} in namespace {namespace_id}"
            )

    def _read_namespace(self, namespace_id: str) -> Namespace:
        """
        Lazily construct a Namespace object on read.
        :param namespace_id: The namespace identifer
        :return: The Namespace object
        """
        self._ensure_namespace_exists(namespace_id)
        return Namespace(
            identifier=namespace_id,
            models=[
                self._read_model(namespace_id, id)
                for id in self.list_models(namespace_id)
            ],
        )

    def _read_model(self, namespace_id: str, model_id: str) -> Model:
        """
        Lazily construct a Model object on read.
        :param namespace_id: The namespace identifier
        :param model_id: The model identifier
        :return: The model object
        """
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)
        return Model(
            identifier=model_id,
            versions=[
                self._read_version(namespace_id, model_id, id)
                for id in self.list_versions(namespace_id, model_id)
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
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)
        self._ensure_version_exists(namespace_id, model_id, version_id)
        return Version(identifier=version_id)

    # -------------------------------------------------------------------------
    # Artifacts
    # -------------------------------------------------------------------------

    def write_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
    ) -> ArtifactModel:
        artifacts = self._get_version_artifacts(
            namespace_id, model_id, version_id
        )
        if artifact.header.identifier in artifacts:
            raise errors.ErrorAlreadyExists(
                f"Artifact '{artifact.header.identifier}'"
            )

        self.storage.write_json_to_file(
            self._artifact_path(
                namespace_id, model_id, version_id, artifact.header.identifier
            ),
            artifact.dict(),
        )
        return artifact

    def read_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        artifacts = self._get_version_artifacts(
            namespace_id, model_id, version_id
        )

        self._ensure_artifact_exists(artifact_id, artifacts)
        return ArtifactModel(
            **self.storage.read_json_file(
                self._artifact_path(
                    namespace_id, model_id, version_id, artifact_id
                )
            )
        )

    def read_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ArtifactModel]:
        artifacts = self._get_version_artifacts(
            namespace_id, model_id, version_id
        )
        return [
            ArtifactModel(
                **self.storage.read_json_file(
                    self._artifact_path(
                        namespace_id, model_id, version_id, artifact_id
                    )
                )
            )
            for artifact_id in artifacts
        ][offset : offset + limit]

    def search_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> list[ArtifactModel]:
        artifacts = self.read_artifacts(namespace_id, model_id, version_id)
        return [
            artifact for artifact in artifacts if query.filter.match(artifact)
        ]

    def delete_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        artifact = self.read_artifact(
            namespace_id, model_id, version_id, artifact_id
        )
        self.storage.delete_file(
            self._artifact_path(
                namespace_id, model_id, version_id, artifact.header.identifier
            )
        )
        return artifact

    def _ensure_artifact_exists(
        self, artifact_id: str, artifacts: list[str]
    ) -> None:
        """Throws an ErrorNotFound if the given artifact does not exist."""
        if artifact_id not in artifacts:
            raise errors.ErrorNotFound(f"Artifact {artifact_id}")

    def _get_version_artifacts(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> list[str]:
        """
        Get artifacts for a version from storage.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the version
        :raises ErrorNotFound: If the required structural elements are not present
        :return: The associated artifacts
        """
        self._ensure_namespace_exists(namespace_id)
        self._ensure_model_exists(namespace_id, model_id)
        self._ensure_version_exists(namespace_id, model_id, version_id)

        return [
            a.stem
            for a in self.storage.list_json_files(
                self._base_path(namespace_id, model_id, version_id)
            )
        ]

    def _base_path(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Path:
        """
        Format a local FS path to a version of a model of a namespace.
        :param namespace_id: The namespace identifier
        :param model_id: The model identifier
        :param version_id: The version identifier
        :return: The formatted path
        """
        return Path(self.root, namespace_id, model_id, version_id)

    def _artifact_path(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ):
        """
        Formats a local FS path to an artifact.
        :param namespace_id: The namespace identifier
        :param model_id: The model identifier
        :param version_id: The version identifier
        :param artifact_id: The artifact identifier
        :return: The formatted path
        """
        return Path(
            self._base_path(namespace_id, model_id, version_id),
            artifact_id + ".json",
        )


class LocalFileSystemStore(Store):
    """A local file system implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = JsonFileStorage()
        """The underlying storage for the store."""

    def session(self) -> LocalFileSystemStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return LocalFileSystemStoreSession(self.uri.uri, storage=self.storage)
