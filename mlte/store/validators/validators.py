"""Collection of inter store validation implementations."""

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.catalog.model import CatalogEntry
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.error import ErrorNotFound
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.store.validators.composite_validator import CrossValidator

import mlte.store.artifact.store as ArtifactStore
import mlte.store.custom_list.store as CustomListStore


class ArtifactUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an artifact against the user store."""

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
        
        with ManagedUserSession(self.user_store.session()) as session:
            # TODO: Make sure this is always valid, it is what we do in the simple demo, maybe some other places
            if new_artifact.header.creator:
                try:
                    session.user_mapper.read(new_artifact.header.creator)
                except ErrorNotFound:
                    raise RuntimeError(f"Artifact creator validation failure. User: {new_artifact.header.creator} not found.")
        
        return new_artifact

class ArtifactCustomListValidator(CrossValidator):
    """Implementation of a CrossValidator to validate an artifact against the custom list store."""

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
            if new_artifact.header.type == ArtifactType.NEGOTIATION_CARD:
                for requirement in new_artifact.body.system_requirements:
                    # TODO: Determine if this should be allowed to be empty str or not. Is defaulted to None in model
                    #   if it is allowed to be empty, this will have to not error for the frontend
                    if requirement.quality != "":
                        try:
                            session.custom_list_entry_mapper.read(requirement.quality, CustomListName.QUALITY_ATTRIBUTES)
                        except ErrorNotFound:
                            raise RuntimeError(f"Artifact quality attribute validation failure. Custom list entry: {requirement.quality} not found.")

        return new_artifact

class CatalogUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an catalog entry against the user store."""

    def __init__(
        self,
        artifact_store: ArtifactStore = None,
        user_store: UserStore = None,
        custom_list_store: CustomListStore = None,
    ):
        super().__init__(user_store=user_store)

    def validate(self, new_entry: CatalogEntry) -> CatalogEntry:
        if self.user_store == None:
            raise RuntimeError("Catalog user validator's user store has not been set.")
        
        with ManagedUserSession(self.user_store.session()) as session:
            try:
                session.user_mapper.read(new_entry.header.creator)
            except ErrorNotFound:
                raise RuntimeError(f"Catalog creator validation failure. User: {new_entry.header.creator} not found.")
            
            try:
                session.user_mapper.read(new_entry.header.updater)
            except ErrorNotFound:
                raise RuntimeError(f"Catalog creator validation failure. User: {new_entry.header.creator} not found.")
        
        return new_entry

class CatalogCustomListValidator(CrossValidator):
    """Implementation of CrossValidator to validate a catalog entry against custom list store."""

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
        
        with ManagedCustomListSession(self.custom_list_store.session()) as session:
            try:
                session.custom_list_entry_mapper.read(new_entry.quality_attribute, CustomListName.QUALITY_ATTRIBUTES)
            except ErrorNotFound:
                raise RuntimeError(f"Catalog entry quality attribute validation failure. Custom list entry: {new_entry.quality_attribute} not found.")

        return new_entry
