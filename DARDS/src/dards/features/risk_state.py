# M = --
# Risk state inference.
# Direction-first interpretation with persistence awareness.

from dards.types import MarketSnapshot
from dards.features.persistence import directional_persistence


def infer_risk_state(snapshot: MarketSnapshot) -> str:
    """
    Classifies market environment using directional persistence.

    Step 1: assess repeated equity behaviour
    Step 2: assess repeated duration behaviour
    Step 3: combine into capital environment lens
    """

    # For now we simulate short lookback using current return only.
    # Later this will ingest rolling return history.

    equity_series = [snapshot.returns.get("SPY",0)]
    duration_series = [snapshot.returns.get("TLT",0)]

    equity_persistence = directional_persistence(equity_series)
    duration_persistence = directional_persistence(duration_series)

    # Persistent equity strength vs duration weakness
    if equity_persistence > 0 and duration_persistence < 0:
        return "risk_on"

    # Persistent defensive behaviour
    if equity_persistence < 0 and duration_persistence > 0:
        return "risk_off"

    return "neutral"