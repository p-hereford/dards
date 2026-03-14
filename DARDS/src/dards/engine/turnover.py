# Y = -.--
# Turnover control.
# Dampens allocation changes to reduce trading intensity and implementation drag.

from typing import Dict, Tuple


def apply_turnover_control(
    prev: Dict[str, float],
    new: Dict[str, float],
    max_turnover: float,
) -> Tuple[Dict[str, float], float]:
    """
    Applies a simple turnover cap using convex mixing.

    max_turnover:
        maximum allowed sum(|w_new - w_prev|)

    Returns:
        (adjusted_weights, realised_turnover)
    """

    if not prev:
        turnover = sum(abs(w) for w in new.values())
        return new, turnover

    turnover = sum(abs(new.get(a,0.0) - prev.get(a,0.0)) for a in set(prev) | set(new))

    if turnover <= max_turnover:
        return new, turnover

    # Scale changes down to meet turnover constraint
    if turnover == 0:
        return new, 0.0

    alpha = max_turnover / turnover

    adjusted = {}
    for a in set(prev) | set(new):
        adjusted[a] = prev.get(a,0.0) + alpha * (new.get(a,0.0) - prev.get(a,0.0))

    realised = sum(abs(adjusted.get(a,0.0) - prev.get(a,0.0)) for a in set(prev) | set(new))

    return adjusted, realised