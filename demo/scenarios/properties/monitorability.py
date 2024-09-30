
from mlte.property.base import Property


class Monitorability(Property):
    """
    The Interoperability property reflects contract requirements on model interfaces.
    """

    def __init__(self, rationale: str):
        """Initialize a Interoperability instance."""
        super().__init__(
            instance=self,
            description="""
            The Monitorability property assesses the monitoring requirements of a
            model and system. These requirements may be expressed in a variety of ways,
            including requriements on line formats in log files, timestamps, and log content. 
                """,
            rationale=rationale,
        )