"""Enum of the predefined custom list names."""

from __future__ import annotations

from typing import Optional

from strenum import StrEnum


class CustomListName(StrEnum):
    """Custom lists names."""

    QA_CATEGORIES = "qa_categories"
    QUALITY_ATTRIBUTES = "quality_attributes"


class CustomListNameDict(dict[CustomListName, CustomListName]):
    def __setitem__(
        self: "CustomListNameDict",
        key: CustomListName,
        value: CustomListName,
    ):
        if isinstance(key, CustomListName) and isinstance(
            value, CustomListName
        ):
            super().__setitem__(key.value, value.value)
        else:
            raise KeyError(f"CustomListName {key} or {value} is not valid.")

    def __getitem__(self, key) -> CustomListName:
        if key in CustomListName._value2member_map_:
            return super().__getitem__(key)
        else:
            raise KeyError(f"CustomListName {key} is not valid.")


class CustomListParentMappings:
    parent_mappings = CustomListNameDict()

    parent_mappings[CustomListName.QUALITY_ATTRIBUTES] = (
        CustomListName.QA_CATEGORIES
    )

    @staticmethod
    def get_child_list_name(
        list_name: Optional[CustomListName],
    ) -> Optional[CustomListName]:
        """Gets the name of the child list of list_name."""
        if (
            list_name
            and list_name in CustomListParentMappings.parent_mappings.values()
        ):
            child_list_name = list(
                CustomListParentMappings.parent_mappings.keys()
            )[
                list(CustomListParentMappings.parent_mappings.values()).index(
                    list_name
                )
            ]
            return child_list_name
        else:
            return None
