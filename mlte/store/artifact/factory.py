"""Top-level functions for artifact store creation."""

from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.base import StoreType, StoreURI


def create_artifact_store(parsed_uri: StoreURI) -> ArtifactStore:
    """
    Create a MLTE artifact store instance.
    :param parsed_uri: The URI for the store instance
    :return: The store instance
    """
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryStore(parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return LocalFileSystemStore(parsed_uri)
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        return HttpArtifactStore(uri=parsed_uri)
    if parsed_uri.type == StoreType.RELATIONAL_DB:
        # Import is here to avoid importing SQL libraries if they have not been installed.
        from mlte.store.artifact.underlying.rdbs.store import (
            RelationalDBArtifactStore,
        )

        return RelationalDBArtifactStore(parsed_uri)
    else:
        raise Exception(
            f"Artifact store can't be created, unknown or unsupported URI type received for uri {parsed_uri}"
        )
