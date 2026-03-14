# H = ....
# Market data provider interface.
# Defines how external data sources connect to DARDS.
# Explicitly separates observation time from tradable time to prevent
# forward information leakage.

from datetime import datetime, timezone
from typing import Protocol

from dards.data.schema import MarketDataFrame


class MarketDataProvider(Protocol):
    """
    Interface for any data source feeding the system.

    asof: timestamp at which a decision is being formed.
    The provider must return only information that would have been
    knowable and tradable at that moment.
    """

    def load_snapshot(self, decision_time: datetime) -> MarketDataFrame:
        ...