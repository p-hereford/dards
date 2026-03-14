# F = ..-.
# Observable market universe definition.
# Establishes which instruments DARDS reads when forming a view of market behaviour.
# This is not a trading universe — it is a sensing surface.

from typing import Tuple


# Initial institutional baseline:
# Equity beta vs duration regime signal.

OBSERVATION_UNIVERSE: Tuple[str,...] = (
    "SPY",  # US equities proxy
    "TLT",  # Long-duration US Treasuries proxy
)
