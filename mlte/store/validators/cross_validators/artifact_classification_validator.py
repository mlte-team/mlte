"""Validator for the classification field of an artifact."""

import typing

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.custom_list.custom_list_names import CustomListName
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.error import ErrorNotFound
from mlte.store.validators.cross_validator import CrossValidator


class ArtifactClassificationValidator(CrossValidator):
    """Implementation of a CrossValidator to validate an artifacts classification against the custom list store."""

    def __init__(
        self,
        custom_list_store: CustomListStore,
    ):
        """
        Initialize a ArtifactCLassificationValidator instance.
        :param custom_list_store: Custom list store store to use for validation.
        """
        self.custom_list_store = custom_list_store

    def validate(self, new_artifact: ArtifactModel) -> None:
        print("validating")

        with ManagedCustomListSession(
            self.custom_list_store.session()
        ) as session:
            if new_artifact.header.type == ArtifactType.NEGOTIATION_CARD:
                card = typing.cast(NegotiationCardModel, new_artifact.body)
                for dataset in card.data:
                    print(dataset.classification)
                    if dataset.classification != "":
                        try:
                            session.custom_list_entry_mapper.read(
                                dataset.classification,
                                CustomListName.CLASSIFICATION,
                            )
                        except ErrorNotFound:
                            raise RuntimeError(
                                f"Artifact classification validation failure. Classification: {dataset.classification} not found. For artifact {new_artifact.header.identifier}."
                            )
