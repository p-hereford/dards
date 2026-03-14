# U = ..-
# Risk budget mapping.
# Converts continuous risk pressure into a bounded institutional volatility target.
# Separation of concerns:
#   1) Map pressure → multiplier
#   2) Map multiplier → bounded volatility target


from dards.types import Confidence
from dards.config.defaults import BASE_VOL_TARGET, MIN_VOL_TARGET, MAX_VOL_TARGET


def risk_budget_multiplier(pressure: float, confidence: Confidence) -> float:
    """
    Returns a multiplier in [0.5, 1.5]

    1.0 → neutral risk budget
    >1  → increase risk budget
    <1  → reduce risk budget
    """

    # Confidence gates aggressiveness
    if confidence == "high":
        cap = 0.5
    elif confidence == "medium":
        cap = 0.35
    else:
        cap = 0.2

    # Map pressure ∈ [-1, +1] into bounded adjustment
    adj = max(-cap, min(cap, pressure * cap))

    return 1.0 + adj


def target_volatility(pressure: float, confidence: Confidence) -> float:
    """
    Converts pressure + confidence into a bounded institutional volatility target.
    """

    multiplier = risk_budget_multiplier(pressure, confidence)

    target = BASE_VOL_TARGET * multiplier
    target = max(MIN_VOL_TARGET, min(target, MAX_VOL_TARGET))

    return target