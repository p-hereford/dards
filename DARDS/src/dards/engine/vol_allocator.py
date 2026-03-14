# W = .--
# Volatility-based allocation engine.
# Converts a target portfolio volatility into asset weights.
# Uses full covariance (via correlation structure) rather than diagonal-only risk.

from typing import Dict
import math

from dards.types import MarketSnapshot, Decision


def allocate_by_vol_target(
    snapshot: MarketSnapshot,
    decision: Decision,
    target_vol: float,
) -> Dict[str, float]:
    """
    Produces a volatility-scaled allocation.

    Mechanics:
    - Inverse volatility base weights (long-only)
    - Portfolio volatility estimated via w' Σ w using snapshot correlation + vol
    - Scale exposure to target_vol

    Returns:
        Dict[asset, weight]
    """

    # --- Step 1: collect vol estimates ---
    vols = {asset: snapshot.vol.get(asset, 0.0) for asset in snapshot.vol}
    vols = {a: v for a, v in vols.items() if v > 0}

    if not vols:
        return {}

    assets = list(vols.keys())

    # --- Step 2: inverse volatility base weights ---
    inv_vol = {a: 1.0 / vols[a] for a in assets}
    inv_sum = sum(inv_vol.values())

    if inv_sum == 0:
        return {}

    base_weights = {a: inv_vol[a] / inv_sum for a in assets}

    # --- Step 3: build covariance from vol + correlation ---
    # cov(i,j) = corr(i,j) * vol(i) * vol(j)
    # If corr missing:
    #   - diag assumed corr=1
    #   - off-diag assumed corr=0 (conservative for diversification claims)
    def corr(i: str, j: str) -> float:
        if i == j:
            return 1.0
        return snapshot.corr.get((i, j), snapshot.corr.get((j, i), 0.0))

    # --- Step 4: portfolio volatility via w' Σ w ---
    port_var = 0.0
    for i in assets:
        for j in assets:
            port_var += base_weights[i] * base_weights[j] * corr(i, j) * vols[i] * vols[j]

    if port_var <= 0:
        return base_weights

    port_vol = math.sqrt(port_var)

    if port_vol == 0:
        return base_weights

    # --- Step 5: scale to target volatility ---
    scale = target_vol / port_vol
    scaled_weights = {a: base_weights[a] * scale for a in assets}

    return scaled_weights