""" """

from mlte.artifact.model import ArtifactModel
from mlte.catalog.model import CatalogEntry
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.error import ErrorNotFound
from mlte.store.user.store import UserStore
from mlte.store.validators.composite_validator import CrossValidator

import mlte.store.artifact.store as ArtifactStore
import mlte.store.custom_list.store as CustomListStore


class ArtifactUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an Artifact against the User store."""

    def __init__(
        self,
        artifact_store: ArtifactStore = None,
        user_store: UserStore = None,
        custom_list_store: CustomListStore = None,
    ):
        super().__init__(user_store=user_store)

    def validate(self, new_artifact: ArtifactModel) -> ArtifactModel:
        if self.user_store == None:
            raise RuntimeError("Artifact user validator's user store has not been set.")
        ...
        

class ArtifactCustomListValidator(CrossValidator):
    """Implementation of a CrossValidator to validate an Artifact against the Custom List store."""

    def __init__(
        self,
        artifact_store: ArtifactStore = None,
        user_store: UserStore = None,
        custom_list_store: CustomListStore = None,
    ):
        super().__init__(custom_list_store=custom_list_store)

    def validate(self, new_artifact: ArtifactModel) -> ArtifactModel:
        if self.custom_list_store == None:
            raise RuntimeError("Artifact custom list validator's custom list store has not been set.")
        
        with ManagedCustomListSession(self.custom_list_store.session()) as session:
            for requirement in new_artifact.body.system_requirements:
                if requirement.quality != "":
                    try:
                        session.custom_list_entry_mapper.read(requirement.quality, CustomListName.QUALITY_ATTRIBUTES)
                    except ErrorNotFound:
                        raise RuntimeError(f"Artifact quality attribute validation failure. Custom list entry: {requirement.quality} not found.")


class CatalogEntryValidator(CrossValidator):
    """Implementation of CrossValidator to validate a Catalog Entry against Custom List store."""

    def __init__(   
        self,
        artifact_store: ArtifactStore = None,
        user_store: UserStore = None,
        custom_list_store: CustomListStore = None,
    ):
        super().__init__(custom_list_store=custom_list_store)
    
    def validate(self, new_entry: CatalogEntry) -> CatalogEntry:
        if self.custom_list_store == None:
            raise RuntimeError("Catalog custom list validator's custom list store has not been set.")

        print("CATALOGENTRYVALIDATOR")