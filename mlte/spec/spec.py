"""
mlte/spec/spec.py

A collection of properties and their measurements.
"""

from __future__ import annotations

import typing
from typing import Dict, List, Union

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.qa_category.base import QACategory
from mlte.spec.condition import Condition
from mlte.spec.model import QACategoryModel, SpecModel

DEFAULT_SPEC_ID = "default.spec"


def _unique(collection: List[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :return: `True` if all elements are unique, `False` otherwise
    """
    return len(set(collection)) == len(collection)


# -----------------------------------------------------------------------------
# Spec
# -----------------------------------------------------------------------------


class Spec(Artifact):
    """
    The Spec class integrates QACategory, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(
        self,
        identifier: str = DEFAULT_SPEC_ID,
        qa_categories: Dict[QACategory, Dict[str, Condition]] = {},
    ):
        """
        Initialize a Spec instance.

        :param qa_categories: The collection of QACategory that compose the spec, with their conditions keyed by measurement id.
        """
        super().__init__(identifier, ArtifactType.SPEC)

        self.qa_categories = qa_categories
        """The collection of QACategory that compose the Spec."""

        if not _unique([p.name for p in self.qa_categories.keys()]):
            raise RuntimeError("All QACategory in Spec must be unique.")

    # -------------------------------------------------------------------------
    # Serialization.
    # -------------------------------------------------------------------------

    def to_model(self) -> ArtifactModel:
        """Convert a negotation card artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=SpecModel(
                qa_categories=[
                    self._to_qa_category_model(qa_category)
                    for qa_category, _ in self.qa_categories.items()
                ],
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Spec:
        """Convert a negotiation card model to its corresponding artifact."""
        model = typing.cast(ArtifactModel, model)
        assert model.header.type == ArtifactType.SPEC, "Broken precondition."
        body = typing.cast(SpecModel, model.body)
        return Spec(
            identifier=model.header.identifier,
            qa_categories=Spec.to_qa_category_dict(body.qa_categories),
        )

    def _to_qa_category_model(self, qa_category: QACategory) -> QACategoryModel:
        """
        Generate a QACategory model. This just uses QACategory.to_model, but adds the list of conditions.

        :param qa_category: The QACategory of interest
        :return: The QACategory model
        """
        qa_category_model: QACategoryModel = qa_category.to_model()
        qa_category_model.conditions = {
            measurement_id: condition.to_model()
            for measurement_id, condition in self.qa_categories[
                qa_category
            ].items()
        }
        return qa_category_model

    @classmethod
    def to_qa_category_dict(
        cls,
        qa_category_models: List[QACategoryModel],
    ) -> Dict[QACategory, Dict[str, Condition]]:
        """Converts a list of QACategory models, into a dict of properties and conditions."""
        return {
            QACategory.from_model(qa_category_model): {
                measurement_id: Condition.from_model(condition_model)
                for measurement_id, condition_model in qa_category_model.conditions.items()
            }
            for qa_category_model in qa_category_models
        }

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_SPEC_ID

    # -------------------------------------------------------------------------
    # Quality Attribute Category Manipulation
    # -------------------------------------------------------------------------

    def get_qa_category(self, qa_category_id: str) -> QACategory:
        """
        Returns a particular QACategory with the given id.

        :param qa_category_id: The QACategory itself, or its identifier
        :return: The QACategory object.
        """
        qa_categories = [
            category
            for category in self.qa_categories
            if category.name == qa_category_id
        ]
        if len(qa_categories) == 0:
            raise RuntimeError(
                f"QA category {qa_category_id} was not found in list."
            )
        if len(qa_categories) > 1:
            raise RuntimeError(
                f"Multiple properties with same id were found: {qa_category_id}"
            )
        return qa_categories[0]

    def has_qa_category(self, qa_category: Union[QACategory, str]) -> bool:
        """
        Determine if the spec contains a particular QACategory.

        :param qa_category: The QACategory itself, or its identifier
        :return: `True` if the spec has the QACategory, `False` otherwise
        """
        target_name = (
            qa_category if isinstance(qa_category, str) else qa_category.name
        )
        return any(
            qa_category.name == target_name
            for qa_category in self.qa_categories
        )

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Spec instances for equality."""
        if not isinstance(other, Spec):
            return False
        reference: Spec = other
        return self._equal(reference)
