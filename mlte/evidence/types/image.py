"""
mlte/value/types/image.py

A Value instance for image media.
"""

from __future__ import annotations

import base64
import typing
from pathlib import Path
from typing import Union

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType, ImageValueModel
from mlte.model.base_model import BaseModel
from mlte.spec.condition import Condition


class Image(Evidence):
    """
    Image implements the Value interface for image media.
    """

    def __init__(
        self,
        image: Union[str, Path, bytes],
    ):
        """
        Initialize an Image instance.
        :param metadata: The generating measurement's metadata
        :param image: The path to the image (str, Path) or raw image data (bytes)
        """
        if isinstance(image, str):
            image = Path(image)

        if isinstance(image, Path):
            with image.open("rb") as f:
                image = f.read()
        assert isinstance(image, bytes), "Broken invariant."

        super().__init__()

        # TODO(Kyle): Unsure if storing media inline is the
        # right way to go here (not scalable); reassess this.

        self.image: bytes = image
        """The data of the referenced image."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an image value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=ImageValueModel(
                data=base64.encodebytes(self.image).decode("utf-8"),
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Image:
        """
        Convert an opaque value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        model = typing.cast(ArtifactModel, model)
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.value_type == EvidenceType.IMAGE
        ), "Broken Precondition."
        return typing.cast(
            Image,
            Image(
                image=base64.decodebytes(body.value.data.encode("utf-8")),
            ).with_metadata(body.metadata),
        )

    @classmethod
    def register_info(cls, info: str) -> Condition:
        """
        Register info about an image value.
        :param info: The information to record.
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(info=info)
        return condition
