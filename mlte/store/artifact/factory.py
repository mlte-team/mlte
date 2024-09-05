"""
mlte/store/artifact/factory.py

Top-level functions for artifact store creation.
"""


from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBArtifactStore
from mlte.store.base import StoreType, StoreURI


def create_artifact_store(uri: str) -> ArtifactStore:
    """
    Create a MLTE artifact store instance.
    :param uri: The URI for the store instance
    :return: The store instance
    """
    parsed_uri = StoreURI.from_string(uri)
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryStore(parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return LocalFileSystemStore(parsed_uri)
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        return HttpArtifactStore(uri=parsed_uri)
    if parsed_uri.type == StoreType.RELATIONAL_DB:
        return RelationalDBArtifactStore(parsed_uri)
    else:
        raise Exception(
            f"Store can't be created, unknown URI prefix received for uri {parsed_uri}"
        )
