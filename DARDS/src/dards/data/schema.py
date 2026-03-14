# G = --.
# Market data schema.
# Defines how raw observations are structured before entering the decision system.
# Enforces consistency across assets, timestamps, and state variables.

from datetime import datetime, timezone
from typing import Dict

from dards.types import Asset


# Required observable fields for each asset.
# These are measurements, not forecasts.

class MarketDataPoint:
    """
    Single timestamp observation for one asset.
    """

    def __init__(
        self,
        asof: datetime,
        price: float,
        return_1d: float,
        volatility: float,
    ):
        self.asof = asof
        self.price = price
        self.return_1d = return_1d
        self.volatility = volatility


# Cross-asset observation snapshot.
# This structure feeds directly into MarketSnapshot later.

MarketDataFrame = Dict[Asset,MarketDataPoint]
