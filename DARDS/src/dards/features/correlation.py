# S = ...
# Correlation regime inference.
# Evaluates the structural relationship between equity and duration behaviour.

from typing import Dict, Tuple
from dards.types import Asset


def infer_correlation_regime(
    corr: Dict[Tuple[Asset,Asset],float]
) -> str:
    """
    Classifies correlation structure:

    negative → classic risk hedge behaviour
    positive → breakdown / stress regime
    neutral  → weak structural signal
    """

    pair = ("SPY","TLT")

    value = corr.get(pair,0)

    if value < -0.2:
        return "negative"

    if value > 0.2:
        return "positive"

    return "neutral"