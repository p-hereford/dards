# P = .--.
# Decision formation.
# Converts classified market state and posture into a formal
# decision object suitable for desk communication.

from datetime import datetime, timezone
from typing import Tuple

from dards.types import Decision
from dards.types import MarketSnapshot
from dards.engine.posture import map_posture
from dards.engine.risk_budget import risk_budget_multiplier
from dards.features.risk_state import infer_risk_state
from dards.features.confidence import infer_confidence
from dards.features.correlation import infer_correlation_regime
from dards.features.risk_pressure import compute_risk_pressure


def form_decision(snapshot: MarketSnapshot) -> Decision:
    """
    Produces a structured Decision object.

    Incorporates:
    - posture
    - risk stance
    - confidence
    - correlation regime
    - continuous risk pressure
    - risk budget adjustment
    """

    decision_time: datetime = snapshot.asof

    # Core interpretations
    risk_state = infer_risk_state(snapshot)
    posture = map_posture(risk_state)
    confidence = infer_confidence(snapshot)
    corr_regime = infer_correlation_regime(snapshot.corr)

    # Continuous signal
    pressure = compute_risk_pressure(snapshot)

    # Translate pressure into capital risk budget shift
    budget_mult = risk_budget_multiplier(pressure, confidence)

    # Observable behavioural drivers
    key_drivers: Tuple[str,...] = (
        f"SPY return: {snapshot.returns.get('SPY',0):.4f}",
        f"TLT return: {snapshot.returns.get('TLT',0):.4f}",
        f"Correlation regime: {corr_regime}",
        f"Risk pressure: {pressure:.2f}",
    )

    # Known modelling limitations at this stage
    tradeoffs: Tuple[str,...] = (
        "Single-period directional inference",
        "Volatility threshold coarse",
        "Correlation regime static",
        "Pressure based on short horizon inputs",
    )

    expression = (
        f"Capital posture set to {posture} under {risk_state} conditions "
        f"with {corr_regime} equity-duration structure. "
        f"Risk budget multiplier: {budget_mult:.2f}."
    )

    return Decision(
        asof=decision_time,
        posture=posture,
        risk_stance=risk_state,
        confidence=confidence,
        expression=expression,
        tradeoffs=tradeoffs,
        key_drivers=key_drivers,
    )