"""
Superclass for all model properties.
"""


class Property:
    """
    The superclass for all model properties.
    """

    def __init__(self, name: str):
        """
        Initialize a new Property.
        :param name The name of the property
        """
        self.name = name
