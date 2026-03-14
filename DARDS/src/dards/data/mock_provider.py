# I = ..
# Mock market data provider.
# Produces a controlled synthetic snapshot so the system can execute end-to-end
# without external data dependencies.

from datetime import datetime, timezone
import random

from dards.data.schema import MarketDataFrame, MarketDataPoint
from dards.data.universe import OBSERVATION_UNIVERSE


class MockMarketDataProvider:
    """
    Synthetic provider used for structural testing.
    Generates stable but non-deterministic observations.
    """

    def load_snapshot(self, decision_time: datetime) -> MarketDataFrame:

        snapshot: MarketDataFrame = {}

        for asset in OBSERVATION_UNIVERSE:
            price = random.uniform(90,110)
            ret = random.uniform(-0.01,0.01)
            vol = random.uniform(0.1,0.3)

            snapshot[asset] = MarketDataPoint(
                asof=decision_time,
                price=price,
                return_1d=ret,
                volatility=vol,
            )

        return snapshot
