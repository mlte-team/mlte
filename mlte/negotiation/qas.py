"""QAS model and functions to handle Quality Attribute Scenarios."""

from typing import Optional

from pydantic import BaseModel

QAS_ID_PREFIX = "qas_id_"


# -----------------------------------------------------------------------------
# Quality Attribute Scenario Descriptor model.
# -----------------------------------------------------------------------------


class QASDescriptor(BaseModel):
    """Describes the system-level requirements for the model component. Represents a Quality Attribute Scenario."""

    identifier: Optional[str] = None
    """The unique identifier for the QAS."""

    quality: Optional[str] = None
    """System property that is being evaluated."""

    stimulus: Optional[str] = None
    """The condition that triggers this scenario."""

    source: Optional[str] = None
    """Where the stimulus comes from."""

    environment: Optional[str] = None
    """Set of circumnstances in which the scenario takes place."""

    response: Optional[str] = None
    """Activity that ocurrs as the result of the stimulus."""

    measure: Optional[str] = None
    """Used to determine if the goals of the responses of the scenario have been achieved."""


# -----------------------------------------------------------------------------
# Functions to handle the QAS model.
# -----------------------------------------------------------------------------


def _build_qas_id(id_pos: int) -> str:
    """Returns a well formed id for a QAS, based on the prefix and position."""
    # Note we pad the number with up to 2 zeroes.
    return f"{QAS_ID_PREFIX}{id_pos:03d}"


def _get_pos_from_qas_id(qas_id: str) -> int:
    """Returns the position of the QAS id from its name."""
    return int(qas_id.replace(QAS_ID_PREFIX, ""))


def add_qas_ids(quality_scenarios: list[QASDescriptor]) -> list[QASDescriptor]:
    """Ensures that all QAS in the NegotiationCard have an id, and assigns one to those who don't have it."""
    # Find the highest position that has been assigned a QAS id.
    highest_id_pos = 0
    sorted_qas: list[QASDescriptor] = sorted(
        [qas for qas in quality_scenarios if qas.identifier is not None],
        key=lambda x: x.identifier,  # type: ignore
        reverse=True,
    )
    if len(sorted_qas) > 0:
        highest_id_pos = _get_pos_from_qas_id(sorted_qas[0].identifier)  # type: ignore[arg-type]

    # Go over all QAS and assign ids to those that don't have them, based on the highest position found.
    for qas in quality_scenarios:
        if qas.identifier is None:
            highest_id_pos += 1
            qas.identifier = _build_qas_id(highest_id_pos)

    return quality_scenarios
