# A1 = .-
# Drawdown guard.
# Enforces capital preservation logic by scaling risk budget
# when drawdown breaches defined limits.

from typing import Tuple


def apply_drawdown_guard(
    peak_equity: float,
    current_equity: float,
    soft_limit: float = -0.05,
    hard_limit: float = -0.10,
) -> Tuple[float, str]:
    """
    Returns:
        (risk_scale, status)

    risk_scale:
        1.0   → no drawdown constraint
        <1.0  → reduce risk budget

    soft_limit/hard_limit:
        expressed as negative drawdown fractions:
            -0.05 = -5%
            -0.10 = -10%
    """

    if peak_equity <= 0:
        return 1.0, "unknown"

    drawdown = (current_equity / peak_equity) - 1.0

    # No action in normal conditions
    if drawdown >= soft_limit:
        return 1.0, "clear"

    # Soft breach: linear de-risking down to 0.5 at hard limit
    if drawdown > hard_limit:
        span = soft_limit - hard_limit
        severity = (soft_limit - drawdown) / span  # in (0,1)
        scale = 1.0 - 0.5 * severity
        return scale, "soft_breach"

    # Hard breach: cut risk aggressively
    return 0.25, "hard_breach"