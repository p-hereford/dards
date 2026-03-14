# T = -
# Risk pressure scoring.
# Produces a continuous signal describing directional pressure
# after conditioning for persistence, volatility, and structure.

from dards.types import MarketSnapshot
from dards.features.persistence import directional_persistence
from dards.features.correlation import infer_correlation_regime


def compute_risk_pressure(snapshot: MarketSnapshot) -> float:
    """
    Returns a score in [-1, +1]

    +1 → strong pro-risk pressure
    -1 → strong defensive pressure
     0 → neutral / mixed
    """

    equity_series = [snapshot.returns.get("SPY",0)]
    duration_series = [snapshot.returns.get("TLT",0)]

    equity_persistence = directional_persistence(equity_series)
    duration_persistence = directional_persistence(duration_series)

    spy_vol = snapshot.vol.get("SPY",0)
    tlt_vol = snapshot.vol.get("TLT",0)

    corr_regime = infer_correlation_regime(snapshot.corr)

    # Directional base
    directional_component = equity_persistence - duration_persistence

    # Volatility dampening
    vol_penalty = (spy_vol + tlt_vol) / 2

    # Correlation structure
    if corr_regime == "negative":
        corr_adjustment = 0.1
    elif corr_regime == "positive":
        corr_adjustment = -0.1
    else:
        corr_adjustment = 0.0

    score = directional_component - vol_penalty + corr_adjustment

    # Clamp to [-1, +1]
    score = max(-1.0, min(1.0, score))

    return score