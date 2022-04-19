"""
Bind a measurement to one or more properties.
"""

from typing import Union

from ..properties import Property
from ..measurement import Measurement


def bind(measurement: Measurement, *properties: Union[str, Property]):
    """
    Bind a measurement to one or more properties.

    :param measurement: The measurement instance to bind
    :type measurement: Measurement
    :param properties: Properties to which the measurement is bound
    :type properties: Union[str, Property]
    """
    if len(properties) == 0:
        raise RuntimeError(
            "Cannot bind measurement to empty collection of properties."
        )
    property_names = (
        property.name if isinstance(property, Property) else property
        for property in properties
    )
    measurement._bind(*property_names)
