""""""

from abc import ABC, abstractmethod
from typing import Any

import mlte.artifact.artifact as Artifact
from mlte.catalog.model import CatalogEntry
from mlte.store.artifact.store import ArtifactStore
from mlte.store.catalog.store import CatalogStore
from mlte.store.custom_list.store import CustomListStore


class CrossValidator(ABC):
    """"""

    def __init__(self, artifact_store: ArtifactStore = None, catalog_store: CatalogStore = None, custom_list_store: CustomListStore = None):
        """
        Initialize a CrossValidator instance.
        :param artifact_store: Artifact store to use for validation.
        :param catalog_store: Catalog store to use for validation.
        :param custom_list_store: Custom list store store to use for validation.
        """
        self.artifact_store = artifact_store
        self.catalog_store = catalog_store
        self.custom_list_store = custom_list_store

    @abstractmethod
    def validate(self, new_resource: Any) -> Any:
        """
        Validate a resource.
        :param new_resource: The data to create or edit the resource to be validated
        :return: The validated resource
        :raises RuntimeError: On failed validation 
        """
        raise NotImplementedError("Can't validate without a specific implementation.")
    

class ArtifactUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an Artifact against the User store."""

    def validate(self, new_artifact: Artifact.Artifact) -> Artifact.Artifact:
        pass


class CatalogEntryValidator(CrossValidator):
    """Implementation of CrossValidator to validate a Catalog Entry against Custom List store."""

    def validate(self, new_entry: CatalogEntry) -> CatalogEntry:
        print("Validated")


class CompositeValidator:
    """Class to compose CrossValidators."""

    def __init__(self, validators: list[CrossValidator] = []):
        """Initialize a CompositeValidator instance."""

        self.validators = validators
        """List of validators to execute."""

    def validate_all(self) -> None:
        """Validate all validators."""
        for validator in self.validators:
            validator.validate()
