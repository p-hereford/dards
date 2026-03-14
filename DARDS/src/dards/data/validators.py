# J = .---
# Data integrity validators.
# Ensures incoming market observations are structurally safe before
# entering any feature, signal, or decision layer.

from dards.data.schema import MarketDataFrame
from dards.data.universe import OBSERVATION_UNIVERSE


def validate_snapshot(snapshot: MarketDataFrame) -> None:
    """
    Raises exceptions if structural integrity checks fail.
    Designed to fail fast before any modelling or decision logic executes.
    """

    # Universe completeness
    for asset in OBSERVATION_UNIVERSE:
        if asset not in snapshot:
            raise ValueError(f"Missing asset in snapshot: {asset}")

    for asset,data in snapshot.items():

        # Price sanity
        if data.price <= 0:
            raise ValueError(f"Non-positive price for {asset}")

        # Volatility sanity
        if data.volatility < 0:
            raise ValueError(f"Negative volatility for {asset}")

        # Return sanity (guard extreme corruption)
        if abs(data.return_1d) > 0.5:
            raise ValueError(f"Return outlier for {asset}")