"""
test/custom_list/test_model.py

Unit tests for custom_list and custom_list_entry model
"""

from __future__ import annotations

from mlte.custom_list.model import CustomListModel, CustomListEntryModel


# -----------------------------------------------------------------------------
# CustomList
# -----------------------------------------------------------------------------


def test_custom_list() -> None:
    """A custom list can be serialized and dezerialized."""
    objects = [
        CustomListModel(
            name="qa_categories",
            entries=[]
        )
    ]
    for object in objects:
        s = object.to_json()
        d = CustomListModel.from_json(s)
        assert d == object

# -----------------------------------------------------------------------------
# CustomListEntry
# -----------------------------------------------------------------------------

def test_custom_list_entry() -> None:
    """A custom list entry can be serialized and dezerialized."""
    objects = [
        CustomListEntryModel(
            name="Test entry",
            description="Test description"
        )
    ]
    for object in objects:
        s = object.to_json()
        d = CustomListEntryModel.from_json(s)
        assert d == object