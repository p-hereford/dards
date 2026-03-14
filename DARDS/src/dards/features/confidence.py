# R = .-.
# Decision confidence formation.
# Produces a coarse strength signal based on persistence and volatility context.

from dards.types import MarketSnapshot
from dards.features.persistence import directional_persistence


def infer_confidence(snapshot: MarketSnapshot) -> str:
    """
    Determines strength of conviction behind posture.

    high   → persistent + stable volatility
    medium → mixed conditions
    low    → unstable / high-vol environment
    """

    equity_series = [snapshot.returns.get("SPY",0)]
    duration_series = [snapshot.returns.get("TLT",0)]

    equity_persistence = directional_persistence(equity_series)
    duration_persistence = directional_persistence(duration_series)

    spy_vol = snapshot.vol.get("SPY",0)
    tlt_vol = snapshot.vol.get("TLT",0)

    high_vol = spy_vol > 0.30 or tlt_vol > 0.30

    if not high_vol and abs(equity_persistence) > 0 and abs(duration_persistence) > 0:
        return "high"

    if high_vol:
        return "low"

    return "medium"