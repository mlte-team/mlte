"""Validator for the user fields of an artifact."""

from mlte.artifact.model import ArtifactModel
from mlte.store.error import ErrorNotFound
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.store.validators.cross_validator import CrossValidator


class ArtifactUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an artifact against the user store."""

    def __init__(
        self,
        user_store: UserStore,
    ):
        """
        Initialize a ArtifactUserValidator instance.
        :param user_store: User store to use for validation.
        """
        self.user_store = user_store

    def validate(self, new_artifact: ArtifactModel) -> None:
        if new_artifact.header.creator:
            with ManagedUserSession(self.user_store.session()) as session:
                try:
                    session.user_mapper.read(new_artifact.header.creator)
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Artifact creator validation failure. User: {new_artifact.header.creator} not found. For artifact {new_artifact.header.identifier}."
                    )
