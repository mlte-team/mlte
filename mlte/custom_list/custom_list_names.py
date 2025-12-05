"""Enum of the predefined custom list names."""

from __future__ import annotations

from typing import Optional

from strenum import StrEnum


class CustomListName(StrEnum):
    """Class to store hard coded set of Custom List names."""

    CLASSIFICATION = "classification"
    PROBLEM_TYPES = "problem_types"
    TAGS = "tags"
    QA_CATEGORIES = "qa_categories"
    QUALITY_ATTRIBUTES = "quality_attributes"


class CustomListNameDict(dict[CustomListName, CustomListName]):
    """
    Class to create dicts to map one custom list name to another.

    The CustomListNameDict type is used for mapping one custom list name to another.
    This is used to ensure that both key and value are valid CustomListName.
    """

    def __setitem__(
        self: "CustomListNameDict",
        key: CustomListName,
        value: CustomListName,
    ):
        """Override of parent to ensure key and value are valid CustomListName."""
        if isinstance(key, CustomListName) and isinstance(
            value, CustomListName
        ):
            super().__setitem__(key.value, value.value)
        else:
            raise KeyError(f"CustomListName {key} or {value} is not valid.")

    def __getitem__(self, key) -> CustomListName:
        """Override of parent to ensure key is a valid CustomListName."""
        if key in CustomListName._value2member_map_:
            return super().__getitem__(key)
        else:
            raise KeyError(f"CustomListName {key} is not valid.")


class CustomListParentMappings:
    """
    Class to define the parent mappings of custom lists.

    Custom list names, and the parents of each list are set values. This class
    provides a way to define, and then access the parent or child list of
    custom lists.
    """

    parent_mappings = CustomListNameDict()
    """CustomListNameDict to hold all of the mappings."""

    """Setting all of the hard coded parent child relationships."""
    parent_mappings[CustomListName.QUALITY_ATTRIBUTES] = (
        CustomListName.QA_CATEGORIES
    )

    @staticmethod
    def get_parent_list_name(
        list_name: CustomListName,
    ) -> Optional[CustomListName]:
        """Gets the name of the parent list of list_name or None."""
        if list_name and list_name in CustomListParentMappings.parent_mappings:
            return CustomListParentMappings.parent_mappings[list_name]
        else:
            return None

    @staticmethod
    def get_child_list_name(
        list_name: CustomListName,
    ) -> Optional[CustomListName]:
        """Gets the name of the child list of list_name or None."""
        if list_name in CustomListParentMappings.parent_mappings.values():
            child_list_name = list(
                CustomListParentMappings.parent_mappings.keys()
            )[
                list(CustomListParentMappings.parent_mappings.values()).index(
                    list_name
                )
            ]
            return CustomListName(child_list_name)
        else:
            return None
