"""
A Value instance for image media.
"""
from __future__ import annotations

from pathlib import Path
import base64
from typing import Dict, Any, Union

from ..value import Value
from mlte.validation import Validator, Result, Ignore
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata


class Image(Value):
    """
    Image implements the Value interface for image media.
    """

    def __init__(
        self,
        measurement_metadata: MeasurementMetadata,
        image: Union[str, Path, bytes],
    ):
        """
        Initialize an Image instance.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement: MeasurementMetadata
        :param path: The path to the image on disk
        :type path: Union[str, Path]
        """
        if isinstance(image, str):
            image = Path(image)

        if isinstance(image, Path):
            with image.open("rb") as f:
                image = f.read()
        assert isinstance(image, bytes), "Broken invariant."

        super().__init__(self, measurement_metadata)

        # TODO(Kyle): Unsure if storing media inline is the
        # right way to go here (not scalable); reassess this.

        self.image: bytes = image
        """The data of the referenced image."""

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize an Image to a JSON object.

        :return: The JSON object
        :rtype: Dict[str, Any]
        """
        return {"image": base64.encodebytes(self.image).decode("utf-8")}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> Image:
        """
        Deserialize an Image from a JSON object.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement_metadata: MeasurementMetadata
        :param json: The JSON object
        :type json: Dict[str, Any]

        :return: The deserialized instance
        :rtype: Image
        """
        return Image(
            measurement_metadata,
            base64.decodebytes(json["image"].encode("utf-8")),
        )

    def ignore(self, reason: str) -> Result:
        """
        Ignore an image value.

        :param reason: The reason for ignoring the image
        :type reason: str

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Validator(
            "Ignore",
            lambda _: Ignore(reason),
        )(self)
        return result
