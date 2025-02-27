"""
test/custom_list/test_model.py

Unit tests for custom_list and custom_list_entry model.
"""

from __future__ import annotations

import pytest

from mlte.custom_list.custom_list_names import (
    CustomListName,
    CustomListNameDict,
)
from mlte.custom_list.model import CustomListEntryModel, CustomListModel

# -----------------------------------------------------------------------------
# CustomList
# -----------------------------------------------------------------------------


def test_custom_list() -> None:
    """A custom list can be serialized and dezerialized."""
    objects = [CustomListModel(name=CustomListName.QA_CATEGORIES, entries=[])]
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
            description="Test description",
            parent="test parent",
        )
    ]
    for object in objects:
        s = object.to_json()
        d = CustomListEntryModel.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# CustomListNameDict
# -----------------------------------------------------------------------------


def test_custom_list_name_dict() -> None:
    """Test that CustomListNameDict takes keys and values as CustomListNames."""
    test_dict = CustomListNameDict()

    test_dict[CustomListName.QA_CATEGORIES] = None
    test_dict[CustomListName.QUALITY_ATTRIBUTES] = CustomListName.QA_CATEGORIES

    assert test_dict[CustomListName.QA_CATEGORIES] is None
    assert (
        test_dict[CustomListName.QUALITY_ATTRIBUTES]
        == CustomListName.QA_CATEGORIES
    )

    with pytest.raises(Exception):
        test_dict[CustomListName.QA_CATEGORIES] = "value"

    with pytest.raises(Exception):
        test_dict["key"] = CustomListName.QA_CATEGORIEs

    with pytest.raises(Exception):
        test_dict["key"] = "value"

    with pytest.raises(Exception):
        test_dict["key"]
