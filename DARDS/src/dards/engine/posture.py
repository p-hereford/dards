# N = -.
# Capital posture mapping.
# Translates inferred market state into an initial capital stance.
# This is the first step from sensing → action.

from dards.types import Posture


def map_posture(risk_state: str) -> Posture:
    """
    Converts environment classification into capital posture.

    risk_on   → deploy capital
    risk_off  → hold back / defensive
    neutral   → maintain exposure
    """

    if risk_state == "risk_on":
        return "deploy"

    if risk_state == "risk_off":
        return "hold_back"

    return "neutral"