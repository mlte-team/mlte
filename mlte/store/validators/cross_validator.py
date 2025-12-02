from abc import ABC, abstractmethod
from typing import Any, Optional

from mlte.store.custom_list.store import CustomListStore
from mlte.store.user.store import UserStore


class CrossValidator(ABC):
    """Interface to define a CrossValidator that validates store entries against data in separate stores."""

    def __init__(
        self,
        user_store: Optional[UserStore] = None,
        custom_list_store: Optional[CustomListStore] = None,
    ):
        """
        Initialize a CrossValidator instance.
        :param user_store: Catalog store to use for validation.
        :param custom_list_store: Custom list store store to use for validation.
        """
        self.user_store = user_store
        self.custom_list_store = custom_list_store

    @abstractmethod
    def validate(self, new_resource: Any) -> None:
        """
        Validate a resource.
        :param new_resource: The data to create or edit the resource to be validated
        :raises RuntimeError: On failed validation
        """
        raise NotImplementedError(
            "Can't validate without a specific implementation."
        )
