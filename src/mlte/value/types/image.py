"""
A Value instance for image media.
"""
from __future__ import annotations

from pathlib import Path
import base64
from typing import Any, Union

from ..value import Value
from mlte.validation import Condition, Ignore
from mlte.evidence.evidence_metadata import EvidenceMetadata


class Image(Value):
    """
    Image implements the Value interface for image media.
    """

    def __init__(
        self,
        evidence_metadata: EvidenceMetadata,
        image: Union[str, Path, bytes],
    ):
        """
        Initialize an Image instance.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param path: The path to the image on disk
        :type path: Union[str, Path]
        """
        if isinstance(image, str):
            image = Path(image)

        if isinstance(image, Path):
            with image.open("rb") as f:
                image = f.read()
        assert isinstance(image, bytes), "Broken invariant."

        super().__init__(self, evidence_metadata)

        # TODO(Kyle): Unsure if storing media inline is the
        # right way to go here (not scalable); reassess this.

        self.image: bytes = image
        """The data of the referenced image."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize an Image to a JSON object.

        :return: The JSON object
        :rtype: dict[str, Any]
        """
        return {"image": base64.encodebytes(self.image).decode("utf-8")}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json: dict[str, Any]
    ) -> Image:
        """
        Deserialize an Image from a JSON object.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param json: The JSON object
        :type json: dict[str, Any]

        :return: The deserialized instance
        :rtype: Image
        """
        return Image(
            evidence_metadata,
            base64.decodebytes(json["image"].encode("utf-8")),
        )

    @classmethod
    def ignore(self, reason: str) -> Condition:
        """
        Ignore an image value.

        :param reason: The reason for ignoring the image
        :type reason: str

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "Ignore",
            lambda _: Ignore(reason),
        )
        return condition
