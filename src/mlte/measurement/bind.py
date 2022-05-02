"""
Bind a measurement to one or more properties.
"""

from typing import Union

from ..property import Property
from .measurement import Measurement


def bind(
    measurement: Measurement, *properties: Union[str, Property]
) -> Measurement:
    """
    Bind a measurement to one or more properties.

    :param measurement: The measurement instance to bind
    :type measurement: Measurement
    :param properties: Properties to which the measurement is bound
    :type properties: Union[str, Property]

    :return: The bound measurement instance
    :rtype: Measurement
    """
    if len(properties) == 0:
        raise RuntimeError(
            "Cannot bind measurement to empty collection of properties."
        )
    property_names = (
        property if isinstance(property, str) else property.name
        for property in properties
    )
    measurement._bind(*property_names)
    return measurement
