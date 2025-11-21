"""Collection of inter store validation implementations."""

import typing
from typing import Optional

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.catalog.model import CatalogEntry
from mlte.custom_list.custom_list_names import CustomListName
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.artifact.store import ArtifactStore
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.error import ErrorNotFound
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.store.validators.composite_validator import CrossValidator


class ArtifactUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an artifact against the user store."""

    def __init__(
        self,
        artifact_store: Optional[ArtifactStore] = None,
        user_store: Optional[UserStore] = None,
        custom_list_store: Optional[CustomListStore] = None,
    ):
        super().__init__(user_store=user_store)

    def validate(self, new_artifact: ArtifactModel) -> None:
        if self.user_store is None:
            raise RuntimeError(
                "Artifact user validator's user store has not been set."
            )

        if new_artifact.header.creator:
            with ManagedUserSession(self.user_store.session()) as session:
                # TODO: Make sure this is always valid, it is what we do in the simple demo, maybe some other places
                try:
                    session.user_mapper.read(new_artifact.header.creator)
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Artifact creator validation failure. User: {new_artifact.header.creator} not found. For artifact {new_artifact.header.identifier}."
                    )


class ArtifactCustomListValidator(CrossValidator):
    """Implementation of a CrossValidator to validate an artifact against the custom list store."""

    def __init__(
        self,
        artifact_store: Optional[ArtifactStore] = None,
        user_store: Optional[UserStore] = None,
        custom_list_store: Optional[CustomListStore] = None,
    ):
        super().__init__(custom_list_store=custom_list_store)

    def validate(self, new_artifact: ArtifactModel) -> None:
        if self.custom_list_store is None:
            raise RuntimeError(
                "Artifact custom list validator's custom list store has not been set."
            )

        with ManagedCustomListSession(
            self.custom_list_store.session()
        ) as session:
            if new_artifact.header.type == ArtifactType.NEGOTIATION_CARD:
                card = typing.cast(NegotiationCardModel, new_artifact.body)
                for requirement in card.system_requirements:
                    # TODO: Determine if this should be allowed to be empty str or not. Is defaulted to None in model
                    #   if it is allowed to be empty, this will have to not error for the frontend
                    if (
                        requirement.quality != ""
                        and requirement.quality is not None
                    ):
                        try:
                            session.custom_list_entry_mapper.read(
                                requirement.quality,
                                CustomListName.QUALITY_ATTRIBUTES,
                            )
                        except ErrorNotFound:
                            raise RuntimeError(
                                f"Artifact quality attribute validation failure. Custom list entry: {requirement.quality} not found. For artifact {new_artifact.header.identifier}."
                            )


class CatalogUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an catalog entry against the user store."""

    def __init__(
        self,
        artifact_store: Optional[ArtifactStore] = None,
        user_store: Optional[UserStore] = None,
        custom_list_store: Optional[CustomListStore] = None,
    ):
        super().__init__(user_store=user_store)

    def validate(self, new_entry: CatalogEntry) -> None:
        if self.user_store is None:
            raise RuntimeError(
                "Catalog user validator's user store has not been set."
            )

        with ManagedUserSession(self.user_store.session()) as session:
            if new_entry.header.creator is not None:
                try:
                    session.user_mapper.read(new_entry.header.creator)
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog creator validation failure. User: {new_entry.header.creator} not found. For catalog entry {new_entry.header.identifier}."
                    )

            # TODO: Ensure this is valid, this is how we start catalog entries
            if (
                new_entry.header.updater is not None
                and new_entry.header.updater != ""
            ):
                try:
                    session.user_mapper.read(new_entry.header.updater)
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog creator validation failure. User: {new_entry.header.updater} not found. For catalog entry {new_entry.header.identifier}."
                    )


class CatalogCustomListValidator(CrossValidator):
    """Implementation of CrossValidator to validate a catalog entry against custom list store."""

    def __init__(
        self,
        artifact_store: Optional[ArtifactStore] = None,
        user_store: Optional[UserStore] = None,
        custom_list_store: Optional[CustomListStore] = None,
    ):
        super().__init__(custom_list_store=custom_list_store)

    def validate(self, new_entry: CatalogEntry) -> None:
        if self.custom_list_store is None:
            raise RuntimeError(
                "Catalog custom list validator's custom list store has not been set."
            )

        # TODO: Determine if this should be allowed to be empty str or not. Is defaulted to None in model
        #   if it is allowed to be empty, this will have to not error for the frontend
        if (
            new_entry.quality_attribute != ""
            and new_entry.quality_attribute is not None
        ):
            with ManagedCustomListSession(
                self.custom_list_store.session()
            ) as session:
                try:
                    session.custom_list_entry_mapper.read(
                        new_entry.quality_attribute,
                        CustomListName.QUALITY_ATTRIBUTES,
                    )
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog entry quality attribute validation failure. Custom list entry: {new_entry.quality_attribute} not found. For catalog entry {new_entry.header.identifier}."
                    )
