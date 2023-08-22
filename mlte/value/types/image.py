"""
mlte/value/types/image.py

A Value instance for image media.
"""

from __future__ import annotations

import base64
import typing
from pathlib import Path
from typing import Union

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.validation.condition import Condition
from mlte.validation.result import Ignore
from mlte.value.artifact import Value
from mlte.value.model import ImageValueModel, ValueModel, ValueType


class Image(Value):
    """
    Image implements the Value interface for image media.
    """

    def __init__(
        self,
        metadata: EvidenceMetadata,
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

        super().__init__(self, metadata)

        # TODO(Kyle): Unsure if storing media inline is the
        # right way to go here (not scalable); reassess this.

        self.image: bytes = image
        """The data of the referenced image."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an image value artifact to its corresponding model.
        :return: The artifact model
        """
        return ArtifactModel(
            header=ArtifactHeaderModel(
                identifier=self.identifier, type=self.type
            ),
            body=ValueModel(
                artifact_type=ArtifactType.VALUE,
                metadata=self.metadata,
                value=ImageValueModel(
                    value_type=ValueType.IMAGE,
                    data=base64.encodebytes(self.image).decode("utf-8"),
                ),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Image:  # type: ignore[override]
        """
        Convert an opaque value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        assert model.header.type == ArtifactType.VALUE, "Broken Precondition."
        body = typing.cast(ValueModel, model.body)

        assert body.value.value_type == ValueType.IMAGE, "Broken Precondition."
        return Image(
            metadata=body.metadata,
            image=base64.decodebytes(body.value.data.encode("utf-8")),
        )

    @classmethod
    def ignore(cls, reason: str) -> Condition:
        """
        Ignore an image value.
        :param reason: The reason for ignoring the image
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition(
            "Ignore",
            [reason],
            lambda _: Ignore(reason),
        )
        return condition
