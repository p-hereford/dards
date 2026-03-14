# C1 = -.-.
# Realised risk metrics.
# Tracks realised volatility and checks compliance versus target.

from typing import List, Tuple
import math


def realised_vol(returns: List[float], window: int = 20, annualisation: int = 252) -> float:
    """
    Rolling realised volatility estimate from simple returns.

    returns:
        list of period returns (e.g. daily)

    window:
        lookback length for realised vol

    annualisation:
        scale factor (252 for daily)
    """

    if len(returns) < 2:
        return 0.0

    slice_ = returns[-window:] if len(returns) >= window else returns

    n = len(slice_)
    if n < 2:
        return 0.0

    mean = sum(slice_) / n
    var = sum((r - mean) ** 2 for r in slice_) / (n - 1)

    return math.sqrt(var) * math.sqrt(annualisation)


def vol_compliance(realised: float, target: float, tolerance: float = 0.15) -> Tuple[bool, float]:
    """
    Checks whether realised vol is within a tolerance band around target.

    tolerance:
        0.15 → ±15% band

    Returns:
        (within_band, gap)
    """

    if target <= 0:
        return False, realised - target

    lower = target * (1.0 - tolerance)
    upper = target * (1.0 + tolerance)

    within = (lower <= realised <= upper)
    gap = realised - target

    return within, gap