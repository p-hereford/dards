# K = -.-
# Market snapshot assembler.
# Converts validated raw observations into the canonical MarketSnapshot
# structure consumed by the decision engine.

from datetime import datetime, timezone
from typing import Dict,Tuple

from dards.types import MarketSnapshot, Asset
from dards.data.schema import MarketDataFrame


def assemble_snapshot(
    decision_time: datetime,
    data: MarketDataFrame,
    correlation: Dict[Tuple[Asset,Asset],float],
) -> MarketSnapshot:
    """
    Transforms raw provider output into the canonical system snapshot.
    Correlation is passed explicitly to avoid hidden estimation.
    """

    prices = {asset:point.price for asset,point in data.items()}
    returns = {asset:point.return_1d for asset,point in data.items()}
    vol = {asset:point.volatility for asset,point in data.items()}

    return MarketSnapshot(
        asof=decision_time,
        prices=prices,
        returns=returns,
        vol=vol,
        corr=correlation,
    )