"""
mlte/custom_list/custom_list_names.py

Enum of the predefined custom list names.
"""

from __future__ import annotations

from strenum import StrEnum


class CustomListName(StrEnum):
    """Custom lists names."""

    QA_CATEGORIES = "qa_categories"
    QUALITY_ATTRIBUTES = "quality_attributes"

class CustomListNameDict(dict):
    def __set_item__(self: "CustomListNameDict", key: CustomListName, value: CustomListName):
        if isinstance(key, CustomListName):
            super().__setitem__(key, value)
        else:
            raise KeyError(f"CustomListName {key} is not valid.")
        
    def __getitem__(self, key):
        if isinstance(key, CustomListName):
            return super().__getitem__(key)
        else:
            raise KeyError(f"CustomListName {key} is not valid.")
        
class CustomListParentMappings:
    parent_mappings = CustomListNameDict()

    parent_mappings[CustomListName.QA_CATEGORIES] = None
    parent_mappings[CustomListName.QUALITY_ATTRIBUTES] = CustomListName.QA_CATEGORIES